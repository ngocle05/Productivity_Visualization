"""
CSC 201 - Nifty Project: Productivity Visualization
Author: Ngoc Le

Assistance Documentation:
    - Dr.Stonedahl gave suggestion about data types, helped me to fix problems with text objects and suggested me to use pickle.
    
Code from the Internet and other sources:
    - The code for the Button class is taken from Project 3.
    - I learned about pickle from https://wiki.python.org/moin/UsingPickle
    - I learned how to check if a file exists from https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions

"""

from graphics2 import *
from constants import *
import random
import time
import pickle
import os.path

from button import Button
from dailyVisualization import dailyBarChart
from weeklyVisualization import weeklyBarChart

def validateUserNumberEntry(entry, minValidNum, maxValidNum):
    """ The function checks whether a given Entry object
        has an integer in it AND that the integer is within a valid range.
        It returns True for valid, and False for invalid.
    """
    entryStr = entry.getText()
    if entryStr.isdigit() and minValidNum <= int(entryStr) <= maxValidNum:
        return True
    else:
        return False
    
    
def validateUserTextEntry(entry, validTextList):
    """ The function checks whether a given Entry object
        has a string in it AND that the string is within a valid list.
        It returns True for valid, and False for invalid.
    """
    entryStr = entry.getText()
    if entryStr in validTextList:
        return True
    else:
        return False
    
    
def displayOpeningScreen():  
    """ Displays the program introduction.
        The user clicks the "Start" button to start using the program.

    """ 
    window = GraphWin("Productivity Visualization", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('azure')
    
    welcomeText = Text(Point(WINDOW_WIDTH/2, 100),'Welcome to Productivity Visualization!')
    welcomeText.setSize(30)
    welcomeText.setTextColor('salmon')
    welcomeText.setStyle('bold')
    welcomeText.draw(window)
    
    introductionText = Text(Point(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 100),'What you can do with this program:\n'
                                                                      + '\n'
                                                                      + '* See the visualization of your daily productivity.\n'
                                                                      + '* See the visualization of your weekly productivity.')
    
    noteText = Text(Point(WINDOW_WIDTH/2, WINDOW_HEIGHT/2),'NOTE:    You can only use one account for this program!')
    
    introductionText.setTextColor('lightcoral')
    introductionText.setSize(17)
    introductionText.draw(window)
    
    noteText.setSize(10)
    noteText.setTextColor('red')
    noteText.draw(window)
    
    startButton = Button(Point(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100),300,100,"Start")
    startButton.draw(window)
    startButton.activate()
    
    clickPt = window.getMouse()
    while not startButton.isClicked(clickPt):
        clickPt = window.getMouse()
    window.close()


def createUserInfoFile(userName, numCourse, courseToColorDict): 
    """ The function creates an empty dictionary maps the userName to a tuple of the number of courses the user is taking and a dict.
        Then, it writes the dictionary to a pickle file. e.g. {'ngoc':(2,{'csc':'red','math':'pink'})}
        The function returns the file name.
        
        Parameters:
        userName: the user's name
        numCourse: the number of course that the user is taking
        courseToColorDict: a dictionary maps each course to its color
        
    """
    userInfoDict = {}
    userInfoDict[userName] = (numCourse, courseToColorDict)
    fileName = "userInfoFile.txt"
    pickle.dump(userInfoDict, open(fileName,'wb'))
    
    return fileName


def createUserDataFile(userName): 
    """ The function creates an empty dictionary which will map a tuple of week and day to a list which maps the course to the percent of completed tasks for that course.
        e.g. { (1, 'Monday') : {'CSC': 80, 'MATH': 50} }
        Then, it writes the dictionary to a pickle file.
        The function returns the file name.
        
        Parameters:
        userName: the user's name
        
    
    """
    DayWeekToCoursePercentDict = {}
    fileName = 'ProductivityData.txt'
    pickle.dump(DayWeekToCoursePercentDict, open(fileName,'wb'))
    
    return fileName


def getUserInfo(userInfoFile):
    """ The function get user's information from the file created from the function createUserInfoFile().
        It returns the user's name, the number of courses that the user is taking and a dictionary which maps each course to its color.
        
        Parameters:
        userInfoFile: the file created from createUserDataFile()
        
    """
    userInfoDict = pickle.load(open(userInfoFile,'rb'))
    for user in userInfoDict:
        userName = user
        numCourse = userInfoDict[user][0]
        courseToColorDict = userInfoDict[user][1]
        
        return userName, numCourse, courseToColorDict
    
    
def displayAccountScreen(userName = "", numCourse = 0, courses = ()):  
    """ The function asks the user to register if the user doesn't have an account or to log in if the user already has one.
        If the user chooses to register, he/she will have to input the userName, numCourse and the course's names.
        Then, create a file for user's information by calling the function createUserInfoFile().
        The functions will also creates a userDataFile by calling the function createUserDataFile().
        If the user chooses to log in, the function getUserInfo() will be called to get userName, numCourse, courseToColorDict.
        
        The function returns userName, numCourse, courseToColorDict, userDataFile.
         
    """
    window = GraphWin("Productivity Visualization", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('azure')
    
    instructionText =  Text(Point(WINDOW_WIDTH/2, 50),'')
    instructionText.setTextColor('salmon')

    registerButton = Button(Point(WINDOW_WIDTH/4, 150),300,100,"Register")
    registerButton.draw(window)
    registerButton.activate()
    
    loginButton = Button(Point(3*(WINDOW_WIDTH/4), 150),300,100,"Login")
    loginButton.draw(window)
    loginButton.activate()
    
    # check if an account exists
    if not os.path.isfile("userInfoFile.txt"):
        loginButton.deactivate()
        instructionText.setText('Click Register to create an account!')
    else:
        registerButton.deactivate()
        instructionText.setText('You already have an account.\n'
                              + 'Click Login to continue!')
    
    instructionText.draw(window)
    
    clickPt = window.getMouse()
    while not (registerButton.isClicked(clickPt) or loginButton.isClicked(clickPt)): 
        instructionText.setTextColor('red')
        clickPt = window.getMouse()
        
        if registerButton.isClicked(clickPt) or loginButton.isClicked(clickPt):   
            instructionText.undraw()
    
    stepList = ['enter userName','enter numCourse','enter coursesName']
    
    if registerButton.isClicked(clickPt):
        y = 250
        for step in stepList:
            if step == 'enter userName':
                instructionText = "Enter your username and click!"
            elif step == 'enter numCourse':
                instructionText = "Enter the number of courses (1-6) and click!"
            else:
                instructionText = "Enter names of courses seperated by ',' and click!\n" + "(CSC,MATH)"
            
            text = Text(Point(WINDOW_WIDTH/4, y),f"{instructionText}")
            text.setSize(15)
            text.draw(window)
            
            entry = Entry(Point(WINDOW_WIDTH/4, y+50),20)
            entry.setSize(15)
            entry.draw(window)
            
            errorText = Text(Point(WINDOW_WIDTH/4, y+100),"")
            errorText.setTextColor('red')
            errorText.draw(window)
        
            window.getMouse()
            if step == 'enter numCourse':
                while not validateUserNumberEntry(entry, 1, 6):
                    errorText.setText(f"{instructionText}")
                    window.getMouse()
                    if validateUserNumberEntry(entry, 1, 6):
                        errorText.setText("")
            else:
                while entry.getText() == "":
                    errorText.setText(f"{instructionText}")
                    window.getMouse()
                    if entry.getText() != "":
                        errorText.setText("")
            y += 150
            
            window.getMouse()
            
            if step == 'enter userName':
                userName = entry.getText()
            elif step == 'enter numCourse':
                numCourse = int(entry.getText())
            else:
                courses = entry.getText()
                
            
        courseList = courses.split(',')
        
        # create a dict which maps each course to its color
        courseToColorDict = {}
        for i in range (len(courseList)):
            courseToColorDict[courseList[i]] = COLOR_LIST[i]

        createUserInfoFile(userName, numCourse, courseToColorDict)
        userDataFile = createUserDataFile(userName)
        window.close()
        
        return userName, numCourse, courseToColorDict, userDataFile 

        
    elif loginButton.isClicked(clickPt):

        userName, numCourse, courseToColorDict = getUserInfo("userInfoFile.txt")
        userDataFile = 'ProductivityData.txt'
        window.close()
        
        return userName, numCourse, courseToColorDict, userDataFile


def displayMenuScreen(userName):
    """ The function asks the user to click buttons to see a bar chart of daily productivity or weekly productivity.
        The function returns the user's choice.
        
        Parameters:
        userName: the user's name
        
    """
    userChoice = ""
    
    window = GraphWin("Productivity Visualization", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('azure')
    
    # display instruction
    instructionText = Text(Point(WINDOW_WIDTH/2, 200),f"{userName}, please click...\n"
                                                    + '\n'
                                                    + "* The first button, if you want to see a bar chart of your daily productivity.\n"
                                                    + "* The second button, if you want to see a bar chart of your weekly productivity.\n")
    instructionText.setSize(20)
    instructionText.setTextColor('salmon')
    instructionText.draw(window)
    

    # display menu buttons
    dailyVisualizationButton = Button(Point(WINDOW_WIDTH/4, WINDOW_HEIGHT - 100),300,100,"Daily Productivity\n" + "Visualization")
    dailyVisualizationButton.draw(window)
    dailyVisualizationButton.activate()
    
    weeklyVisualizationButton = Button(Point(3*(WINDOW_WIDTH/4), WINDOW_HEIGHT - 100),300,100,"Weekly Productivity\n" + "Visualization")
    weeklyVisualizationButton.draw(window)
    weeklyVisualizationButton.activate()
    
    errorText2 = Text(Point(WINDOW_WIDTH/2, 500),"")
    errorText2.setTextColor('red')
    errorText2.draw(window)
    
    clickPt = window.getMouse()
    if not (dailyVisualizationButton.isClicked(clickPt) or weeklyVisualizationButton.isClicked(clickPt)):
        while userChoice == "":
            errorText2.setText("Please click a button!")
            clickPt = window.getMouse()
            
            if dailyVisualizationButton.isClicked(clickPt):
                userChoice = "Daily Productivity Visualization"
            elif weeklyVisualizationButton.isClicked(clickPt):
                userChoice = "Weekly Productivity Visualization"
                
            if dailyVisualizationButton.isClicked(clickPt) or weeklyVisualizationButton.isClicked(clickPt):  
                errorText2.setText("")
                window.close()
    else:
        if dailyVisualizationButton.isClicked(clickPt):
            userChoice = "Daily Productivity Visualization"
        elif weeklyVisualizationButton.isClicked(clickPt):
            userChoice = "Weekly Productivity Visualization"

        window.close()

    return userChoice


def chooseDayAndWeek():
    """ The function asks the user to enter the Week and the day on which he/she wants to see a visualization of productivity.
        The function returns the week and the day that the user enters.
        
    """
    
    window = GraphWin("Choose Day and Week", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('azure')
    
    nextButton = Button(Point(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100),200,70,"Next")
    nextButton.draw(window)
    nextButton.activate()
    
    # instruction
    weekText = Text(Point(WINDOW_WIDTH/2, TOP_MARGIN),f"Click after entering Week and Day!")
    weekText.setSize(15)
    weekText.setTextColor('red')
    weekText.draw(window)
    
    weekText = Text(Point(WINDOW_WIDTH/2, TOP_MARGIN+100),f"Enter Week (1-15)")
    weekText.setTextColor('salmon')
    weekText.setSize(15)
    weekText.draw(window)
    
    weekEntry = Entry(Point(WINDOW_WIDTH/2, TOP_MARGIN+150),20)
    weekEntry.setSize(15)
    weekEntry.draw(window)
    
    dayText = Text(Point(WINDOW_WIDTH/2, TOP_MARGIN+250),f"Enter Day of Week (Monday-Friday)")
    dayText.setTextColor('salmon')
    dayText.setSize(15)
    dayText.draw(window)
    
    dayEntry = Entry(Point(WINDOW_WIDTH/2, TOP_MARGIN+300),20)
    dayEntry.setSize(15)
    dayEntry.draw(window)
    
    errorText = Text(Point(WINDOW_WIDTH/2, TOP_MARGIN + 400),"")
    errorText.setTextColor('red')
    errorText.draw(window)
    
    weekValid = False
    dayValid = False
    
    while not (weekValid and dayValid):
        window.getMouse()
        weekValid = validateUserNumberEntry(weekEntry, 1, 15)
        dayValid = validateUserTextEntry(dayEntry, WEEK_DAY_LIST)
        
        if not (weekValid and dayValid):
            errorText.setText(f"Please enter Week and Day in the correct ranges!")
        else:      
            errorText.setText("")
    
        
    clickPt = window.getMouse()
    while not nextButton.isClicked(clickPt):
        clickPt = window.getMouse()
    window.close()
        
    return int(weekEntry.getText()), dayEntry.getText()


def chooseWeek():
    """ The function asks the user to enter the Week and the day on which he/she wants to see a visualization of productivity.
        The function returns the week and the day that the user enters.
        
    """
    window = GraphWin("Choose Week", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('azure')
    
    nextButton = Button(Point(WINDOW_WIDTH/2, WINDOW_HEIGHT - 100),200,70,"Next")
    nextButton.draw(window)
    nextButton.activate()
    
    weekText = Text(Point(WINDOW_WIDTH/2, TOP_MARGIN),f"Click after entering the Week!")
    weekText.setSize(15)
    weekText.setTextColor('red')
    weekText.draw(window)
    
    weekText = Text(Point(WINDOW_WIDTH/2, TOP_MARGIN+100),f"Enter Week (1-15)")
    weekText.setSize(15)
    weekText.setTextColor('salmon')
    weekText.draw(window)
    
    weekEntry = Entry(Point(WINDOW_WIDTH/2, TOP_MARGIN+150),20)
    weekEntry.setSize(15)
    weekEntry.draw(window)
    
    errorText = Text(Point(WINDOW_WIDTH/2, TOP_MARGIN + 400),"")
    errorText.setTextColor('red')
    errorText.draw(window)
    
    weekValid = False
    
    while not weekValid:
        window.getMouse()
        weekValid = validateUserNumberEntry(weekEntry, 1, 15)
    
        if not weekValid :
            errorText.setText(f"Please enter Week and Day in the correct ranges!")
        else:      
            errorText.setText("")
    
        
    clickPt = window.getMouse()
    while not nextButton.isClicked(clickPt):
        clickPt = window.getMouse()
    window.close()
        
    return int(weekEntry.getText())


def isDataAvailable(week, day, userDataFile):
    """ The function checks if the data for the given week and day is available in the userDataFile.
        The function returns True if the data is available and False if it is not.
        
        Parameters:
        week: the week that the users chooses to check
        day: the day that the users chooses to check
        userDataFile: the file which is created from the function createUserDataFile().
                      The file contains a dictionary maps a tuple of (the week and the day) to another dictionary which maps the course to the percent on that day/ week.
    
    """ 
    DayWeekToCoursePercentDict = pickle.load(open(userDataFile,'rb'))
    if (week,day) in DayWeekToCoursePercentDict:
        return True
    else:
        return False
    
    
def inputDataforADay(numCourse, courseToColorDict, week, day, userDataFile, window):
    """ The function asks the users to input the percent of completed tasks for each course on a given day.

        Parameters:
        numCourse: the number of courses that the user is taking
        courseToColorDict: a dictionary which maps each course to its color.
        week: the week that the user want to input data
        day: the day of the week that the user want to input data
        userDataFile: the file which is created from the function createUserDataFile().
                      The file contains a dictionary maps a tuple of (the week and the day) to another dictionary which maps the course to the percent on that day/ week.
        
    """
    DayWeekToCoursePercentDict = pickle.load(open(userDataFile,'rb'))
    DayWeekToCoursePercentDict[(week, day)] = {}
    
    # percent
    percentText = Text(Point(WINDOW_WIDTH/2, TOP_MARGIN),f"Enter Percent (0-100) of completed tasks for each course")
    percentText.setSize(15)
    percentText.draw(window)
    
    y = TOP_MARGIN + 50
    
    for course in courseToColorDict:

        courseText = Text(Point(WINDOW_WIDTH/2 - 150 , y),f"{course}")
        courseText.setSize(15)
        courseText.draw(window)
        
        courseEntry = Entry(Point(WINDOW_WIDTH/2, y),10)
        courseEntry.setSize(15)
        courseEntry.draw(window)
        
        
        errorText = Text(Point(WINDOW_WIDTH/2, y + 50),"")
        errorText.setTextColor('red')
        errorText.draw(window)
        
        window.getMouse()
        while not validateUserNumberEntry(courseEntry, 0, 100):
            errorText.setText(f"Please enter Percent and Click")
            window.getMouse()
            if validateUserNumberEntry(courseEntry, 0, 100):
                errorText.setText("")
                
        y += 50
    
        percent = int(courseEntry.getText())
        DayWeekToCoursePercentDict[(week, day)][course] = percent

    pickle.dump(DayWeekToCoursePercentDict, open(userDataFile,'wb'))


def inputDataForDailyProductivity(numCourse, courseToColorDict, week, day, userDataFile):
    """ The function checks whether the data for the day that the user wants to see the visualization exists.
        If not, call the function inputDataforADay() to input data.
        Else, close the window.
        
        Parameters:
        numCourse: the number of courses that the user is taking
        courseToColorDict: a dictionary which maps each course to its color.
        week: the week that the user want to input data
        day: the day of the week that the user want to input data
        userDataFile: the file which is created from the function createUserDataFile().
                      The file contains a dictionary maps a tuple of (the week and the day) to another dictionary which maps the course to the percent on that day/ week.
        
    """
    window = GraphWin(f"Productivity on {day} - Week {week}", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('azure')

    if not isDataAvailable(week, day, userDataFile):
        inputDataforADay(numCourse, courseToColorDict, week, day, userDataFile, window)
        
        button = Button(Point(WINDOW_WIDTH/2, TOP_MARGIN+500),300,70,"See visualization")
        button.draw(window)
        button.activate()
        
        clickPt = window.getMouse()
        while not button.isClicked(clickPt):
            clickPt = window.getMouse()
        window.close()

    else:
        window.close()

def checkDataforAWeek(week, userDataFile):
    """ The function checks whether the data for a current week exists.
        The function returns 2 lists: a list contains days on which the data is available and a list contains days on which the data is not available.
        
        Parameters:
        week: the week that the user want to check whether data exists
        userDataFile: the file which is created from the function createUserDataFile().
                      The file contains a dictionary maps a tuple of (the week and the day) to another dictionary which maps the course to the percent on that day/ week.
        
    """
    availableDataDay = []
    unavailableDataDay = []
    for day in WEEK_DAY_LIST:
        if isDataAvailable(week, day, userDataFile):
            availableDataDay.append(day)
        else:
            unavailableDataDay.append(day)
    
    return availableDataDay, unavailableDataDay
    

def inputDataForWeeklyProductivity(numCourse, courseToColorDict, week, userDataFile):
    """ The function checks whether the data for the week that the user wants to see the visualization exists.
        If the number of days on which the data is unvailable on that week != 0 and less than 7, the user can choose to input the data or see the visualization without updating the missing data.
        If the number of days on which the data is unvailable on that week is 7 (no data for all 7 days on that week), the user need to update the data.
        If the data for 7 days on that week is available, close the window.
        The funtion also updates on the data on which day is available and returns availableDataDay, unavailableDataDay
        
        Parameters:
        numCourse: the number of courses that the user is taking
        courseToColorDict: a dictionary which maps each course to its color.
        week: the week that the user want to input data
        userDataFile: the file which is created from the function createUserDataFile().
                      The file contains a dictionary maps a tuple of (the week and the day) to another dictionary which maps the course to the percent on that day/ week.
    
    """
    window = GraphWin(f"Productivity on Week {week}", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('azure')
    
    updateDataButton = Button(Point(WINDOW_WIDTH/4, TOP_MARGIN+500),300,70,"Update Data")
    updateDataButton.draw(window)
    updateDataButton.activate()
    
    visualizationButton = Button(Point(3*(WINDOW_WIDTH/4), TOP_MARGIN+500),300,70,"See visualization")
    visualizationButton.draw(window)
    visualizationButton.activate()
    
    instructionText = Text(Point(WINDOW_WIDTH/2, 200),'')
    
    availableDataDay, unavailableDataDay = checkDataforAWeek(week, userDataFile)
    if len(unavailableDataDay) != 0 :
        if len(unavailableDataDay) < 7:
            instructionText.setText(f'Data for {len(unavailableDataDay)} days on Week {week} is not available.\n'
                                   +'\n'
                                   + 'Click "Update Data" if you want to update data for those days\n'
                                   + 'Click "See visualization" if you want to see the visualization without updating the data.')
        else:
            instructionText.setText(f'Data for Week {week} is not available.\n'
                                   + f'Click "Update Data" to update data for Week {week}\n')
            visualizationButton.deactivate()
        
        instructionText.setTextColor('salmon')
        instructionText.draw(window)
        
        clickPt = window.getMouse()
        while not (updateDataButton.isClicked(clickPt) or visualizationButton.isClicked(clickPt)):
            clickPt = window.getMouse()
            
        if updateDataButton.isClicked(clickPt):
            window.close()
            for day in unavailableDataDay:
                window = GraphWin(f"Productivity Visualization on {day}", WINDOW_WIDTH, WINDOW_HEIGHT)
                window.setBackground('azure')
                
                text = Text(Point(WINDOW_WIDTH/2,TOP_MARGIN - 100 ),f"{day} - Week {week}")
                text.setSize(30)
                text.draw(window)
                
                
                inputDataforADay(numCourse, courseToColorDict, week, day, userDataFile, window)
                
                nextButton = Button(Point(WINDOW_WIDTH/2, TOP_MARGIN+500),300,70,"Next")
                nextButton.draw(window)
                nextButton.activate()
                
                clickPt = window.getMouse()
                while not nextButton.isClicked(clickPt):
                    clickPt = window.getMouse()
                window.close()
                
                availableDataDay.append(day)
                                 
        elif visualizationButton.isClicked(clickPt):
            window.close()
        
    else:
        window.close()
        
    return availableDataDay
    
    
def displayDailyProductivity(userName, courseToColorDict, week, day, userDataFile):
    """ The function draws the bar chart representing the daily productivity on the day that the user chose. 
        
        Parameters:
        numCourse: the number of courses that the user is taking
        courseToColorDict: a dictionary which maps each course to its color.
        week: the week that the user want to see the visualization
        day: the day of the week that the user want to see the visualization
        userDataFile: the file which is created from the function createUserDataFile().
                      The file contains a dictionary maps a tuple of (the week and the day) to another dictionary which maps the course to the percent on that day/ week.
    """
    
    window = GraphWin(f" {userName}'s Daily Productivity", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('white')
    barChart = dailyBarChart(userName, courseToColorDict, week, day, userDataFile)
    barChart.draw(window)
    
    nextButton = Button(Point(WINDOW_WIDTH - 70, WINDOW_HEIGHT - 40),100,40,"Next")
    nextButton.draw(window)
    nextButton.activate()
    
    clickPt = window.getMouse()
    while not nextButton.isClicked(clickPt):
        clickPt = window.getMouse()
    window.close()
        
def displayWeeklyProductivity(userName, courseToColorDict, week, availableDataDay, userDataFile):
    """ The function draws the bar chart representing the weekly productivity on the week that the user chose. 
        
        Parameters:
        numCourse: the number of courses that the user is taking
        courseToColorDict: a dictionary which maps each course to its color.
        week: the week that the user want to see the visualization
        userDataFile: the file which is created from the function createUserDataFile().
                      The file contains a dictionary maps a tuple of (the week and the day) to another dictionary which maps the course to the percent on that day/ week.
    """
    window = GraphWin(f" {userName}'s Weekly Productivity", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('white')
    barChart = weeklyBarChart(userName, courseToColorDict, week, availableDataDay, userDataFile)
    barChart.draw(window)

    nextButton = Button(Point(WINDOW_WIDTH - 70, WINDOW_HEIGHT - 40),100,40,"Next")
    nextButton.draw(window)
    nextButton.activate()
    
    clickPt = window.getMouse()
    while not nextButton.isClicked(clickPt):
        clickPt = window.getMouse()
    window.close()
    

def displayClosingScreeen():
    """ The function asks the user to click a button to see continue using the program or to close it.
        The function returns True if the user chooses continue. Else, return false.

    """
    window = GraphWin("Productivity Visualization", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setBackground('azure')
    
    instructionText = Text(Point(WINDOW_WIDTH/2, 200),f"please click...\n"
                                                    + '\n'
                                                    + "* The first button, if you want to continue using the program.\n"
                                                    + "* The second button, if you want to close the porgam.\n")
    instructionText.setTextColor('salmon')
    instructionText.setSize(20)
    instructionText.draw(window)

    # display buttons
    continueButton = Button(Point(WINDOW_WIDTH/4, WINDOW_HEIGHT - 100),300,70,"Continue")
    continueButton.draw(window)
    continueButton.activate()
    
    quitButton = Button(Point(3*(WINDOW_WIDTH/4), WINDOW_HEIGHT - 100),300,70,"Quit")
    quitButton.draw(window)
    quitButton.activate()
    
    clickPt = window.getMouse()
    while not (continueButton.isClicked(clickPt) or quitButton.isClicked(clickPt)):
        clickPt = window.getMouse()
        
    window.close()
    
    if continueButton.isClicked(clickPt):
        return True
    elif quitButton.isClicked(clickPt):
        return False
    
    
def main():
    displayOpeningScreen()
    userName, numCourse, courseToColorDict, userDataFile  = displayAccountScreen()
    continueUsingProgram = True
    while continueUsingProgram:
        userChoice = displayMenuScreen(userName)
        
        if userChoice == "Daily Productivity Visualization":
            week, day = chooseDayAndWeek()
            inputDataForDailyProductivity(numCourse, courseToColorDict, week, day, userDataFile)
            displayDailyProductivity(userName, courseToColorDict, week, day, userDataFile)
        else:
            week = chooseWeek()
            availableDataDay = inputDataForWeeklyProductivity(numCourse, courseToColorDict, week, userDataFile)
            displayWeeklyProductivity(userName, courseToColorDict, week, availableDataDay, userDataFile)
            
        continueUsingProgram = displayClosingScreeen()
            
        
if __name__ == '__main__':    
    main()

























