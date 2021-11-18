#################################################
# Your name:Rohit Chand
# Your andrew id:rchand
#################################################
from cmu_112_graphics import *

import calendar
from datetime import *
from tkcalendar import *
from tkinter import *
import calendar
import json
import os


class Event(object):

    def __init__(self,name,date,time):
        self.eventName = name
        self.eventDate = date
        self.eventTime = time

    def __repr__(self):
        return f'{self.eventName} {self.eventDate} {self.eventTime}'

def appStarted(app):
    app.isWelcomeScreen = True
    app.isEventScreen = False
   
    app.rows, app.cols, app.marginRight, app.marginLeft, app.marginTop, app.marginBottom = calDimensions()
    app.cal = calendar.TextCalendar(firstweekday = 6)
   
    app.currentMonth = datetime.now().month
    app.realMonth = datetime.now().month

    app.currentYear = datetime.now().year
    app.realYear = datetime.now().year

    today = date.today()
    app.date = today.strftime("%d")

    app.day = today.weekday()
    app.scheduledDayOfWeek = "Thursday"
    
    app.events = []

    app.data_path = "event data.json"
    if os.path.exists(app.data_path):
        with open(app.data_path, 'r') as f:
            app.acts = json.load(f)
    else:
        app.acts = {}

    app.eventColors = ["red", "yellow", "magenta", "pink","cyan", "green", "orange"]
    app.daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" ]

def mousePressed(app, event):
    #Welcome Screen
    if (0 < event.x < app.width) :
        app.isWelcomeScreen = False
        app.isEventScreen = True

    #Event/Calendar Screen
    if (app.marginRight - 50 < event.x < app.marginRight - 30) and (10 < event.y < 30):
        getEvent(app)

    if app.isEventScreen == True and ((15 < event.x < 35 and app.height-200-10 < event.y < app.height-200+10)):
        if app.currentMonth - 1 == 0:
            app.currentYear -= 1
            app.currentMonth = 12
        else:
            app.currentMonth -= 1
    if app.isEventScreen == True and ((165 < event.x < 185 and app.height-200-10 < event.y < app.height-200+10)):
        if app.currentMonth + 1 == 13:
            app.currentYear += 1
            app.currentMonth = 1
        else:
            app.currentMonth += 1
    
def calDimensions():
    rows = 48
    cols = 7
    marginRight = 250
    marginLeft = 25
    marginTop = 100
    marginBottom = 25
    return (rows, cols, marginRight,marginLeft,marginTop,marginBottom)

def getEvent(app):
    activity = ""
    date = ""
    time = ""
    activity = app.getUserInput("event: ")
    date = app.getUserInput("date: MM/DD/YY")
    time = app.getUserInput("time: ")
    app.events.append(Event(activity,date,time))
    if date not in app.acts:
        app.acts[date] = [activity, time]
    else:
        app.acts[date].append(activity, time)
    with open(app.data_path, 'w') as f:
        json.dump(app.acts, f)

def drawWelcomeScreen(app,canvas):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        canvas.create_rectangle(0,0,app.width,app.height,fill = '#1d1d1d')
        canvas.create_text(app.width//2, app.height*7//16, 
                                text = f"{current_time}",
                                font = "Helvetica 52",
                                fill = '#dddddd')
        canvas.create_text(app.width//2, app.height*9//16, 
                                text = f"Welcome Rohit!",
                                font = "Helvetica 52",
                                fill = '#dddddd')

def drawBackground(app,canvas):
        canvas.create_rectangle(0,0,app.width,app.height,fill = '#1d1d1d')
        canvas.create_rectangle(0,0,195,app.height,fill = "#292a2c" )

def getCellBounds(app, row, col):
    gridWidth  = app.width - (app.marginRight + app.marginLeft)
    gridHeight = app.height - (app.marginTop + app.marginBottom)
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.marginRight + col * cellWidth
    x1 = app.marginRight + (col+1) * cellWidth
    y0 = app.marginTop + row * cellHeight
    y1 = app.marginTop + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def drawCell(app, canvas, row, col):
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_rectangle(x0-1, y0-1, x1+1, y1+1, fill = '#3d3d3d',
                                                    width = 0)
    canvas.create_rectangle(x0, y0, x1, y1, fill = '#1d1d1d',
                                            width = 0)

def drawCal(app, canvas):
    drawWeekdays(app,canvas)
    for col in range(app.cols):
        for row in range(app.rows):
            drawCell(app, canvas, row, col)

def drawTitle(app,canvas):
    if app.realMonth == 1:   
        month = "Janurary"
    if app.realMonth == 2:
        month = "February"
    if app.realMonth == 3:
        month = "March"
    if app.realMonth == 4:
        month = "April"
    if app.realMonth == 5:
        month = "May"
    if app.realMonth == 6:
        month = "June"
    if app.realMonth == 7:
        month = "July"
    if app.realMonth == 8:
        month = "August"
    if app.realMonth == 9:
        month = "September"
    if app.realMonth == 10:
        month = "October"
    if app.realMonth == 11:
        month = "November"
    if app.realMonth == 12:
        month = "December"

    year = app.realYear
    x = app.marginRight - 50
    y = 50
    canvas.create_text(x,y,text = f"{month} {year}",
                           font = "Helvetica 32 bold",
                           fill = '#dddddd',
                           anchor = W)


def drawTime(app,canvas):
    amORPm = "AM"
    x0 = app.marginRight - 50
    x1 = app.marginRight
    gridHeight = app.height - (app.marginTop + app.marginBottom)
    cellHeight = gridHeight / app.rows * 2
    for row in range(app.rows//2):
        if row >= 12:
            amORPm = "PM"
        y0 = app.marginTop + row * cellHeight
        y1 = app.marginTop + (row+1) * cellHeight
        time = row%12
        if time == 0:
            time = 12
        canvas.create_text(x1 - 30,y0, text = f"{time} {amORPm}",
                                                  fill = '#484848')

def drawWeekdays(app,canvas):
    y = app.marginTop - 15
    gridWidth  = app.width - (app.marginRight + app.marginLeft)
    cellWidth = gridWidth / app.cols
    date = int(app.date)
    day = (int(app.day) + 1)%7
    for col in range(len(app.daysOfWeek)):
        x0 = app.marginRight + col * cellWidth
        x1 = app.marginRight + (col+1) * cellWidth
        x = (x0 + x1)//2
        canvas.create_text(x,y, text = f'{app.daysOfWeek[col]} {date - day + col}',
                                font = 'Helvetica 20',
                                fill = '#dddddd')

        if (app.realYear == app.currentYear and 
                    app.realMonth == app.currentMonth and 
                    str(date - day + col) == app.date):
                    canvas.create_oval(x + 7, y - 14, x + 35, y + 14, fill = "#ff453a", width = 0)
                    canvas.create_text(x + 20,y, text = f'{date - day + col}',
                                font = 'Helvetica 20',
                                fill = '#210908')

def drawEvents(app,canvas):
    if app.scheduledDayOfWeek == "Sunday":
        col = 0
    elif app.scheduledDayOfWeek == "Monday":
        col = 1
    elif app.scheduledDayOfWeek == "Tuesday":
        col = 2
    elif app.scheduledDayOfWeek == "Wednesday":
        col = 3
    elif app.scheduledDayOfWeek == "Thursday":
        col = 4
    elif app.scheduledDayOfWeek == "Friday":
        col = 5
    elif app.scheduledDayOfWeek == "Saturday":
        col = 6
    gridWidth  = app.width - (app.marginRight + app.marginLeft)
    cellWidth = gridWidth / app.cols
    gridHeight = app.height - (app.marginTop + app.marginBottom)
    cellHeight = gridHeight / app.rows * 2
    x0 = app.marginRight + col * cellWidth
    x1 = app.marginRight + (col+1) * cellWidth

    for dates in app.acts:
        dash = app.acts[dates][1].find("-")
        time = app.acts[dates][1]
        startTime, endTime = float(time[:dash]), float(time[dash+1:])
        y0 = app.marginTop + startTime * cellHeight
        y1 = app.marginTop + endTime * cellHeight
        canvas.create_rectangle(x0,y0,x1,y1,fill = '#344244',
                                            width = 0)
        canvas.create_rectangle(x0,y0,x0+5,y1,fill = '#9fe1e7',
                                            width = 0)
        canvas.create_text(x0 + 10,y0 + 10, text = f"{app.acts[dates][0]}",
                                                font = "Helvetica 12 bold",
                                                fill = '#9fe1e7',
                                                anchor = W)

def drawMiniCal(app,canvas):

        calendarView = app.cal.formatmonth(app.currentYear,app.currentMonth).split(" ")
        calendarViewPrintable = []

        for element in calendarView:
            if "\n" in element:
                for val in element.split("\n"):
                    calendarViewPrintable.append(val)
            else:
                calendarViewPrintable.append(element)
        while '' in calendarViewPrintable:
            calendarViewPrintable.remove('')
        
        #display month and year
        canvas.create_text(100,app.height-200,text = f"{calendarViewPrintable[0]} {calendarViewPrintable[1]}",
                                              font = "Helvetica 14 bold",
                                              fill = "#9f9fa0")

        #display days of week
        for x in range(2,9):
            canvas.create_text(25*(x-2)+25,app.height - 175,text = f"{calendarViewPrintable[x][0]}", 
                                                            font = "Helvetica 14 bold",
                                                            fill = '#dddddd')

        #get first day of the month
        first_weekday, num_days_in_month = calendar.monthrange(app.currentYear, app.currentMonth)

        #display dates
        if first_weekday == 6:
            for date in range(9,len(calendarViewPrintable)):
                canvas.create_text(25*(((date-9)%7))+25,app.height - 150 + ((date-9)//7)*25,
                                    text = f'{calendarViewPrintable[date]}',
                                    font = "Helvetica 12",
                                    fill = "#dddddd")
                #display red circle behind current date
                if (app.realYear == app.currentYear and 
                    app.realMonth == app.currentMonth and 
                    calendarViewPrintable[date] == app.date):
                    canvas.create_oval(25*(((date-9)%7))+26 - 10,app.height - 150 + ((date-9)//7)*25 - 10,
                                     25*(((date-9)%7))+26 + 10,app.height - 150 + ((date-9)//7)*25 + 10,
                                    fill = "#ff453a",
                                    width = 0)
                    canvas.create_text(25*(((date-9)%7))+25,app.height - 150 + ((date-9)//7)*25,
                                    text = f'{calendarViewPrintable[date]}',
                                    font = "Helvetica 12",
                                    fill = "#210908")
        else:
            for date in range(9,len(calendarViewPrintable)):
                canvas.create_text(25*(((date+(first_weekday+1)-9)%7))+25,app.height - 150 + ((date+(first_weekday+1)-9)//7)*25,
                                  text = f'{calendarViewPrintable[date]}',
                                  font = "Helvetica 12",
                                  fill =  "#dddddd")
                #display red circle behind current date
                if (app.realYear == app.currentYear and 
                    app.realMonth == app.currentMonth and 
                    calendarViewPrintable[date] == app.date):
                    canvas.create_oval(25*(((date+(first_weekday+1)-9)%7))+26 - 10,
                                       app.height - 150 + ((date+(first_weekday+1)-9)//7)*25 - 10,
                                       25*(((date+(first_weekday+1)-9)%7))+26 + 10,
                                       app.height - 150 + ((date+(first_weekday+1)-9)//7)*25 + 10,
                                       fill = "#ff453a",
                                       width = 0)
                    canvas.create_text(25*(((date+(first_weekday+1)-9)%7))+25,app.height - 150 + ((date+(first_weekday+1)-9)//7)*25,
                                  text = f'{calendarViewPrintable[date]}',
                                  font = "Helvetica 12",
                                  fill =  "#210908")

        #buttons for next and previous month
        canvas.create_rectangle(15,app.height-200-10,35,app.height-200+10,
                                fill = "#292a2c",
                                width = 0)
        canvas.create_text(25,app.height-202,text =  "<",
                                                  font = "Calibri 14 bold",
                                                  fill = "#9f9fa0")
        canvas.create_rectangle(165,app.height-200-10,185,app.height-200+10,
                                fill = "#292a2c",
                                width = 0)
        canvas.create_text(175,app.height-202,text =  ">",
                                                  font = "Calibri 14 bold",
                                                  fill = "#9f9fa0")

def drawAddEventBtn(app,canvas):
    canvas.create_rectangle(app.marginRight - 50,10,app.marginRight - 30,30,
                                        fill = '#1d1d1d',
                                        width = 0)
    canvas.create_text((app.marginRight - 50 + app.marginRight - 30)//2,(10 + 20)//2,
                                        text = "+",
                                        font = 'Ariel 32',
                                        fill = '#525252')

def redrawAll(app, canvas):
    app.setSize(1440,772)

    if app.isWelcomeScreen == True:
        drawWelcomeScreen(app,canvas)

    elif app.isEventScreen == True:
        drawBackground(app,canvas)
        drawTitle(app,canvas)
        drawTime(app,canvas)
        drawCal(app,canvas)
        drawEvents(app,canvas)
        drawMiniCal(app,canvas)
        drawAddEventBtn(app,canvas)
        
def runCalendar():
    runApp()

def main():
    runApp()

if __name__ == '__main__':
    main()