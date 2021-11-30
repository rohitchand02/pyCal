#################################################
# Your name:Rohit Chand
# Your andrew id:rchand
#################################################
from cmu_112_graphics import *

from datetime import *
from calendar import *
from tkinter import *
import calendar
import time
import pickle
import os
import sys
sys.setrecursionlimit(100000)

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
    
    app.events = []

    app.event_path = "event_data.pickle"
    if os.path.exists(app.event_path):
        with open(app.event_path, 'rb') as f:
            app.acts = pickle.load(f)
    else:
        app.acts = {}

    app.task_path = "task_data.pickle"

    if os.path.exists(app.task_path):
        with open(app.task_path, 'rb') as f:
            app.tasks = pickle.load(f)
    else:
        app.tasks = []

    app.daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    app.displayedDates = set()
    app.realDates = set()

    app.deltaWeek = 0
    app.currentDate = int(app.date)
    app.displayedMonth = datetime.now().month
    app.displayedYear = datetime.now().year

    realWeekdaysToSet(app)
    addDateToSet(app)

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

    if 10 < event.x < 80 and 10 < event.y < 30:
            getTask(app)
            
    if 90 < event.x < 180 and 10 < event.y < 30:
        delTaskEvent(app)

    if 10 < event.x < 180 and 40 < event.y < 70:
        addTasksToCal(app)

    if 1315 < event.x < 1335 and 25 < event.y < 45:
        app.displayedDates.clear()
        app.deltaWeek = -7
        addDateToSet(app)
        print(app.displayedDates)

    if 1340 < event.x < 1390 and 25 < event.y < 45:
        app.displayedDates.clear()
        app.deltaWeek = 0
        app.currentDate = int(app.date)
        app.displayedMonth = datetime.now().month
        app.displayedYear = datetime.now().year
        addDateToSet(app)

    if 1395 < event.x < 1415 and 25 < event.y < 45:
        app.displayedDates.clear()
        app.deltaWeek = 7
        addDateToSet(app)

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
    time = app.getUserInput("time (e.g. 10:00 AM - 2:00 PM): ")
    if date not in app.acts:
        event = [activity, time]
        app.acts[date] = [event]
    else:
        event = [activity, time]
        app.acts[date].append(event)
        
    with open(app.event_path, 'wb') as f:
        pickle.dump(app.acts, f)

def getTask(app):
    task = ""
    date = ""
    time = ""
    priorty = ""
    neededTime = ""
    task = app.getUserInput("task: ")
    date = app.getUserInput("date: MM/DD/YY")
    time = app.getUserInput("time (e.g. 10:00 AM): ")
    priorty = int(app.getUserInput("1. High\n2. Medium\n3. Low "))
    neededTime = float(app.getUserInput("How long do you need to complete this task"))
    inCal = False

    event = [task, date, time, priorty, neededTime, inCal]
    app.tasks.append(event)

    app.tasks = schedule(app.tasks)
        
    with open(app.task_path, 'wb') as f:
        pickle.dump(app.tasks, f)


def delTaskEvent(app):
    taskOrEvent = int(app.getUserInput("Would you like to complete a task or delete an event?\n1. Complete task\n2. Delete event"))
    if taskOrEvent == 1:
        name = app.getUserInput(f"Good job! Which task have you completed? {app.tasks}")
        for x in range(len(app.tasks)):
            if app.tasks[x][0] == name:
                app.tasks.pop(x)
                break
    else:
        date = app.getUserInput("What is the date of the event you would like to delete? (MM/DD/YY)")
        L = []
        for events in app.acts[date]:
            L.append(events[0])
        event = app.getUserInput(f"What event would you like to delete: {L}")
        for x in range(len(app.acts[date])):
            if app.acts[date][x][0] == event:
                app.acts[date].pop(x)

    with open(app.event_path, 'wb') as f:
        pickle.dump(app.acts, f)

    with open(app.task_path, 'wb') as f:
        pickle.dump(app.tasks, f)

#assigns each task a priorty constant
def priortyConstant(task):
    [tasks, deadline, due, priorty, timeNeeded, inCal] = task

    #due date (deadline and time)
    if "12" in due:
        space = due.find(" ")
        due = due[:space]
        
        colon = due.find(":")
        due = f'{int(due[:colon])}:{due[colon+1:]}:00'
        
        currTime = datetime.now().strftime("%H:%M:%S")
    elif "PM" in due:
        space = due.find(" ")
        due = due[:space]
        
        colon = due.find(":")
        due = f'{int(due[:colon])+12}:{due[colon+1:]}:00'
        
        currTime = datetime.now().strftime("%H:%M:%S")
    else:
        space = due.find(" ")
        due = due[:space]

        colon = due.find(":")
        due = f'{int(due[:colon])}:{due[colon+1:]}:00'

        currTime = datetime.now().strftime("%H:%M:%S")

    format = '%Y-%m-%d %H:%M:%S'
    d1 = datetime.strptime(f'20{deadline[6:]}-{deadline[:2]}-{deadline[3:5]} {due}', format)
    d2 = datetime.strptime(f'{date.today()} {currTime}', format)

    d1 = time.mktime(d1.timetuple())
    d2 = time.mktime(d2.timetuple())

    deadlinePri = int(d2-d1) / 60

    if priorty == "1":
        return deadlinePri + 30
    elif priorty == "2":
        return deadlinePri + 20
    else:
        return deadlinePri + 10

#checks if task are ordered properly
def isOrdered(tasks):
    if len(tasks) == 1:
        return True
    for task in range(1,len(tasks)):
        if priortyConstant(tasks[task]) > priortyConstant(tasks[task-1]):
            return False
    return True

#helper to reverse the indexes beteween start and stop in a list
def swaps(tasks, start, stop):
        while (start < stop):
            tasks[start], tasks[stop] = tasks[stop], tasks[start]
            start += 1
            stop -= 1
        return tasks

#finds the next possible order for the tasks
def nextOrder(tasks):
    index = len(tasks)

    for i in reversed(range(0,len(tasks))):
        if tasks[i] > tasks[i-1]:
                index = i - 1
                break
    if index == len(tasks):
        return tasks.reverse()

    for i in reversed(range(index, len(tasks))):
        if tasks[i] > tasks[index]:
            tasks[i], tasks[index] = tasks[index], tasks[i]
            break
    return swaps(tasks,index+1,len(tasks)-1)

#finds all possible permutations of tasks
def permsOfTasks(tasks):
    if (len(tasks) == 0):
        return [[]]
    else:
        tempTasks = permsOfTasks(tasks[1:])
        allTasks = []
        for perm in tempTasks:
            for i in range(len(perm) + 1):
                allTasks.append(perm[:i] + [tasks[0]] + perm[i:])
        return allTasks
    
#backtracking scheduling for to-do tasks   
def schedule(tasks):
    if isOrdered(tasks):
        return tasks
    else:
        solutions = permsOfTasks(tasks)
        solutions.pop(0)
        for solution in solutions:
            if isOrdered(solution):
                return solution
            

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
    if app.displayedMonth == 1:   
        month = "Janurary"
    if app.displayedMonth == 2:
        month = "February"
    if app.displayedMonth == 3:
        month = "March"
    if app.displayedMonth == 4:
        month = "April"
    if app.displayedMonth == 5:
        month = "May"
    if app.displayedMonth == 6:
        month = "June"
    if app.displayedMonth == 7:
        month = "July"
    if app.displayedMonth == 8:
        month = "August"
    if app.displayedMonth == 9:
        month = "September"
    if app.displayedMonth == 10:
        month = "October"
    if app.displayedMonth == 11:
        month = "November"
    if app.displayedMonth == 12:
        month = "December"

    year = app.displayedYear
    x = app.marginRight - 50
    y = 50
    canvas.create_text(x,y,text = f"{month} {year}",
                           font = "Helvetica 32 bold",
                           fill = '#dddddd',
                           anchor = W)

def isOverlapTime(time1, time2):
    return max(0, min(time1[1], time2[1]) - max(time1[0], time2[0]))

def getEarliestAvaibleTime(app, date, deadline, timeNeeded):

    taskEndTime = deadline
    taskColonEnd = taskEndTime.find(":")
    taskAmORPmEnd = taskEndTime.find(" ")

    if int(float(taskEndTime[:taskColonEnd])) == 12:
        taskEndTime = float(taskEndTime[:taskColonEnd]) + float(taskEndTime[taskColonEnd+1:taskAmORPmEnd])/60
    elif "PM" in deadline:
        taskEndTime = float(taskEndTime[:taskColonEnd]) + 12 + float(taskEndTime[taskColonEnd+1:taskAmORPmEnd])/60
    else:
        taskEndTime = float(taskEndTime[:taskColonEnd]) + float(taskEndTime[taskColonEnd+1:taskAmORPmEnd])/60

    for dates in app.acts:
        if dates == date:
            for events in app.acts[dates]:

                dash = events[1].find("-")
                time = events[1]
                startTime, endTime = time[:dash], time[dash+2:]
                colonStart = startTime.find(":")
                amORPmStart = startTime.find(" ")
                colonEnd = endTime.find(":")
                amORPmEnd = endTime.find(" ")

                if "PM" in startTime[amORPmStart:]:
                    startTime = float(startTime[:colonStart]) + 12 + float(startTime[colonStart+1:amORPmStart])/60
                else:
                    startTime = float(startTime[:colonStart]) + float(startTime[colonStart+1:amORPmStart])/60

                if "PM" in endTime[amORPmEnd:]:
                    endTime = float(endTime[:colonEnd]) + 12 + float(endTime[colonEnd+1:amORPmEnd])/60
                else:
                    endTime = float(endTime[:colonEnd]) + float(endTime[colonEnd+1:amORPmEnd])/60          

                if isOverlapTime([taskEndTime-timeNeeded,taskEndTime],[startTime,endTime]) != 0:
                    hour = int(float(taskEndTime-timeNeeded))
                    if hour > 12:
                        hour -= 12
                        amOrPM = 'PM'
                    elif hour == 12:
                        amOrPM = 'PM'
                    else:
                        amOrPM = 'AM'
                    minute = int((startTime%1)-.25*60)
                    
                    return getEarliestAvaibleTime(app, date, f"{int(hour)}:{minute} {amOrPM}", timeNeeded)

    taskStartTime = taskEndTime - timeNeeded

    if int(taskStartTime) == 12:
        minute = int(taskEndTime%1*60)
        taskStartTime = f"{int(taskEndTime)-int(timeNeeded)}:{minute} PM"
    if int(taskStartTime) > 12:
        minute = int(taskStartTime%1*60)
        taskStartTime = f"{int(taskEndTime)-int(timeNeeded)-12}:{minute} PM"
    elif int(taskStartTime) <= 0:
        minute = int(taskStartTime%1*60)
        taskStartTime = f"{int(taskEndTime)-int(timeNeeded)+12}:{minute} AM"
    else:
        minute = int(taskStartTime%1*60)
        taskStartTime = f"{int(taskEndTime)-int(timeNeeded)}:{minute} AM"

    if int(taskEndTime) == 12:
        minute = int(taskEndTime%1*60)
        taskEndTime = f"{int(taskEndTime)}:{minute} PM"
    elif int(taskEndTime) > 12:
        minute = int(taskEndTime%1*60)
        taskEndTime = f"{int(taskEndTime)-12}:{minute} PM"
    elif int(taskEndTime) <= 0:
        minute = int(taskEndTime%1*60)
        taskEndTime = f"{int(taskEndTime)-int(timeNeeded)+12}:{minute} AM"
    else:
        minute = int(taskEndTime%1*60)
        taskEndTime = f"{int(taskEndTime)}:{minute} AM"

    return f"{taskStartTime} - {taskEndTime}"

def addTasksToCal(app):
    for task in app.tasks[::-1]:

        if task[5] == True:
            continue

        activity = task[0]
        date = task[1]
        deadline = task[2]
        timeNeeded = task[4]
        time = getEarliestAvaibleTime(app, date, deadline, timeNeeded)
        task[5] = True

        if date not in app.acts:
            event = [activity, time]
            app.acts[date] = [event]
        else:
            event = [activity, time]
            app.acts[date].append(event)
        
        with open(app.event_path, 'wb') as f:
            pickle.dump(app.acts, f)

        with open(app.task_path, 'wb') as f:
            pickle.dump(app.tasks, f)


def drawTime(app,canvas):
    amORPm = "AM"
    x1 = app.marginRight
    gridHeight = app.height - (app.marginTop + app.marginBottom)
    cellHeight = gridHeight / app.rows * 2
    for row in range(app.rows//2):
        if row >= 12:
            amORPm = "PM"
        y0 = app.marginTop + row * cellHeight
        time = row%12
        if time == 0:
            time = 12
        canvas.create_text(x1 - 30,y0, text = f"{time} {amORPm}",
                                                  fill = '#484848')

def realWeekdaysToSet(app):
    date = app.currentDate + app.deltaWeek

    if date > monthrange(app.displayedYear, app.displayedMonth)[1]:
        if app.displayedMonth == 12:
            app.displayedMonth = 1
            app.displayedYear += 1
            app.currentDate = date%monthrange(app.displayedYear-1, 12)[1]
        else:
            app.displayedMonth += 1
            app.currentDate = date%monthrange(app.displayedYear, app.displayedMonth-1)[1]
    else:
        app.currentDate = date

    if date < 0:
        if app.displayedMonth == 1:
            app.displayedMonth = 12
            app.displayedYear -= 1
            app.currentDate = date + monthrange(app.displayedYear,app.displayedMonth)[1]
        else:
            app.displayedMonth -= 1
            app.currentDate = date + monthrange(app.displayedYear,app.displayedMonth)[1]

    day = (int(app.day) + 1)%7

    for col in range(len(app.daysOfWeek)):
        displayDate = app.currentDate - day + col

        if displayDate > monthrange(app.displayedYear,app.displayedMonth)[1]:
            displayDate %= monthrange(app.displayedYear,app.displayedMonth)[1]
            if int(displayDate) < 10:
                if app.displayedMonth == 12:
                    app.realDates.add(f"1/0{displayDate}/{app.displayedYear&100 + 1}")
                else: 
                    app.realDates.add(f"{app.displayedMonth+1}/0{displayDate}/{app.displayedYear%100}")
            else:
                if app.displayedMonth == 12:
                    app.realDates.add(f"1/{displayDate}/{app.displayedYear&100 + 1}")
                else: 
                    app.realDates.add(f"{app.displayedMonth+1}/{displayDate}/{app.displayedYear%100}")

        elif displayDate < 0:
            if app.displayedMonth == 1:
                displayDate = monthrange(app.displayedYear-1,12)[1]
            else:
                displayDate = monthrange(app.displayedYear,app.displayedMonth-1)[1]

            if app.displayedMonth == 1:
                app.realDates.add(f"12/{displayDate}/{app.displayedYear%100 - 1}")
            else: 
                app.realDates.add(f"{app.displayedMonth}/{displayDate}/{app.displayedYear%100}")

        else:
            if int(displayDate) < 10:
                app.realDates.add(f"{app.displayedMonth}/0{displayDate}/{app.displayedYear%100}")
            else:
                app.realDates.add(f"{app.displayedMonth}/{displayDate}/{app.displayedYear%100}")

def addDateToSet(app):

    date = app.currentDate + app.deltaWeek

    if date > monthrange(app.displayedYear, app.displayedMonth)[1]:
        if app.displayedMonth == 12:
            app.displayedMonth = 1
            app.displayedYear += 1
            app.currentDate = date%monthrange(app.displayedYear-1, 12)[1]
        else:
            app.displayedMonth += 1
            app.currentDate = date%monthrange(app.displayedYear, app.displayedMonth-1)[1]
    elif date <= 0:
        if app.displayedMonth == 1:
            app.displayedMonth = 12
            app.displayedYear -= 1
            app.currentDate = date + monthrange(app.displayedYear,app.displayedMonth)[1]
        else:
            app.displayedMonth -= 1
            app.currentDate = date + monthrange(app.displayedYear,app.displayedMonth)[1]
    else:
        app.currentDate = date

    print(app.displayedMonth, app.currentDate)
    day = (int(app.day) + 1)%7

    for col in range(len(app.daysOfWeek)):
        displayDate = app.currentDate - day + col

        if displayDate > monthrange(app.displayedYear,app.displayedMonth)[1]:
            displayDate %= monthrange(app.displayedYear,app.displayedMonth)[1]
            if int(displayDate) < 10:
                if app.displayedMonth == 12:
                    app.displayedDates.add(f"1/0{displayDate}/{app.displayedYear&100 + 1}")
                else: 
                    app.displayedDates.add(f"{app.displayedMonth+1}/0{displayDate}/{app.displayedYear%100}")
            else:
                if app.displayedMonth == 12:
                    app.displayedDates.add(f"1/{displayDate}/{app.displayedYear&100 + 1}")
                else: 
                    app.displayedDates.add(f"{app.displayedMonth+1}/{displayDate}/{app.displayedYear%100}")

        elif displayDate < 0:
            if app.displayedMonth == 1:
                displayDate = monthrange(app.displayedYear-1,12)[1]
            else:
                displayDate = monthrange(app.displayedYear,app.displayedMonth-1)[1]

            if app.displayedMonth == 1:
                app.displayedDates.add(f"12/{displayDate}/{app.displayedYear%100 - 1}")
            else: 
                app.displayedDates.add(f"{app.displayedMonth}/{displayDate}/{app.displayedYear%100}")

        else:
            if int(displayDate) < 10:
                app.displayedDates.add(f"{app.displayedMonth}/0{displayDate}/{app.displayedYear%100}")
            else:
                app.displayedDates.add(f"{app.displayedMonth}/{displayDate}/{app.displayedYear%100}")

def drawWeekdays(app,canvas):
    y = app.marginTop - 15
    gridWidth  = app.width - (app.marginRight + app.marginLeft)
    cellWidth = gridWidth / app.cols

    day = (int(app.day) + 1)%7


    for col in range(len(app.daysOfWeek)):
        x0 = app.marginRight + col * cellWidth
        x1 = app.marginRight + (col+1) * cellWidth
        x = (x0 + x1)//2

        displayDate = app.currentDate - day + col

        if displayDate > monthrange(app.displayedYear,app.displayedMonth)[1]:
            displayDate %= monthrange(app.displayedYear,app.displayedMonth)[1]

        elif displayDate <= 0:
            displayDate = displayDate + monthrange(app.displayedYear,app.displayedMonth-1)[1]
        

        if int(displayDate) < 10:
            displayDate = f"0{displayDate}"

        canvas.create_text(x,y, text = f'{app.daysOfWeek[col]} {displayDate}',
                                font = 'Helvetica 20',
                                fill = '#dddddd')

        if (app.realYear == app.displayedYear and 
                    app.realMonth == app.displayedMonth and 
                    str(displayDate) == app.date):
                    canvas.create_oval(x + 7, y - 14, x + 35, y + 14, fill = "#ff453a", 
                                                                      width = 0)
                    canvas.create_text(x + 20,y, text = f'{displayDate}',
                                                 font = 'Helvetica 20',
                                                 fill = '#210908')

def drawEvents(app,canvas):

    for dates in app.acts:

        month = int(dates[:2])
        day = int(dates[3:5]) 
        year = int(f"20{dates[6:]}")

        col = (date(year,month,day).weekday() + 1)%7 

        gridWidth  = app.width - (app.marginRight + app.marginLeft)
        cellWidth = gridWidth / app.cols
        gridHeight = app.height - (app.marginTop + app.marginBottom)
        cellHeight = gridHeight / app.rows * 2
        x0 = app.marginRight + col * cellWidth
        x1 = app.marginRight + (col+1) * cellWidth
        dates

        if dates in app.displayedDates:
            for events in app.acts[dates]:
                
                dash = events[1].find("-")
                time = events[1]
                startTime, endTime = time[:dash], time[dash+2:]
                colonStart = startTime.find(":")
                amORPmStart = startTime.find(" ")
                colonEnd = endTime.find(":")
                amORPmEnd = endTime.find(" ")

                if int(startTime[:colonStart]) == 12:
                    startTime = float(startTime[:colonStart]) + float(startTime[colonStart+1:amORPmStart])/60
                elif "PM" in startTime[amORPmStart:]:
                    startTime = float(startTime[:colonStart]) + 12 + float(startTime[colonStart+1:amORPmStart])/60
                else:
                    startTime = float(startTime[:colonStart]) + float(startTime[colonStart+1:amORPmStart])/60

    
                if int(endTime[:colonEnd]) == 12:
                    endTime = float(endTime[:colonEnd]) + float(endTime[colonEnd+1:amORPmEnd])/60

                elif "PM" in endTime[amORPmEnd:]:
                    endTime = float(endTime[:colonEnd]) + 12 + float(endTime[colonEnd+1:amORPmEnd])/60
                else:
                    endTime = float(endTime[:colonEnd]) + float(endTime[colonEnd+1:amORPmEnd])/60

                y0 = app.marginTop + startTime * cellHeight
                y1 = app.marginTop + endTime * cellHeight
                canvas.create_rectangle(x0,y0,x1,y1,fill = '#344244',
                                                    width = 0)
                canvas.create_rectangle(x0,y0,x0+5,y1,fill = '#9fe1e7',
                                                    width = 0)
                canvas.create_text(x0 + 10,y0 + 10, text = f"{events[0]}",
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
        #taken from https://www.kite.com/python/docs/calendar.monthrange
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

def drawCurrentTimeLine(app,canvas):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        colon = current_time.find(":")
        gridHeight = app.height - (app.marginTop + app.marginBottom)
        cellHeight = gridHeight / app.rows * 2
        startTime = float(current_time[:colon]) + float(current_time[colon+1:])/60
        y0 = app.marginTop + startTime * cellHeight
        canvas.create_rectangle(app.marginRight,y0, app.width - app.marginLeft, y0 + 2, 
                                    fill = '#ff453a',
                                    width = 0)

def drawUpcomingTasksTitle(app,canvas):
    canvas.create_text(100, 100, text = "Upcoming tasks",
                                 fill = "#dddddd",
                                 font = "Helvetica 20 bold",
                                 anchor = N)


def drawAddTaskBtn(app,canvas):
    canvas.create_rectangle(10,10,80,30,fill = '#1d1d1d',
                                        width = 0)
    canvas.create_text(45,20,text = "Add task",
                             font = 'Helvetica 12',
                             fill = '#f8f8f8')

def drawTasks(app,canvas):
    for x in range(len(app.tasks)):
        if app.tasks[x][3] == 1:
            priorty = "High"
        elif app.tasks[x][3] == 2:
            priorty = "Medium"
        else:
            priorty = "Low"
            
        canvas.create_rectangle(5, 130 + 70*x, 190, 190 + 70 *x, fill = "#1d1d1d" )

        canvas.create_text(10,70*x + 160,text = f" {x+1}) {app.tasks[x][0]}\nDue:{app.tasks[x][1]} @ {app.tasks[x][2]}\nPriorty: {priorty}",
                                         fill = "#dddddd",
                                         font = "Helvetica 14",
                                         anchor = W)
                                         

def delTaskEventBtn(app,canvas):
    canvas.create_rectangle(90,10,180,30,fill = '#1d1d1d',
                                        width = 0)
    canvas.create_text(135,20,text = "Delete task/event",
                             font = 'Ariel 10',
                             fill = '#f8f8f8')

def drawTaskToCalBtn(app,canvas):
    canvas.create_rectangle(10,40,180,70,fill = '#1d1d1d',
                                        width = 0)
    canvas.create_text(95,55,text = "Add Tasks to Calendar",
                             font = 'Ariel 14',
                             fill = '#f8f8f8')

def drawWeekChangeBtn(app,canvas):
    canvas.create_rectangle(1315,25,1335,45,fill = '#565656',
                                        width = 0)
    canvas.create_text(1325,33,text = "<",
                             font = 'Ariel 14',
                             fill = '#f8f8f8')
    canvas.create_rectangle(1340,25,1390,45,fill = '#565656',
                                        width = 0)
    canvas.create_text(1365,33,text = "Today",
                             font = 'Ariel 14',
                             fill = '#f8f8f8')
    canvas.create_rectangle(1395,25,1415,45,fill = '#565656',
                                        width = 0)
    canvas.create_text(1405,33,text = ">",
                             font = 'Ariel 14',
                             fill = '#f8f8f8')

def drawEventDetails(app,canvas):
    pass

def redrawAll(app, canvas):
    app.setSize(1440,772)

    if app.isWelcomeScreen == True:
        drawWelcomeScreen(app,canvas)

    elif app.isEventScreen == True:
        #calendar
        drawBackground(app,canvas)
        drawTitle(app,canvas)
        drawTime(app,canvas)
        drawCal(app,canvas)
        drawEvents(app,canvas)
        drawMiniCal(app,canvas)
        drawAddEventBtn(app,canvas)
        drawCurrentTimeLine(app,canvas)
        drawWeekChangeBtn(app,canvas)

        #tasks
        drawUpcomingTasksTitle(app,canvas)
        drawAddTaskBtn(app,canvas)
        drawTasks(app,canvas)

        delTaskEventBtn(app,canvas)

        drawTaskToCalBtn(app,canvas)

        if app.mode == 'eventView':
            drawEventDetails(app,canvas)
    
        
def runCalendar():
    runApp()

def main():
    runApp()

if __name__ == '__main__':
    main()