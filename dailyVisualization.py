""" 
This module contains the dailyBarChart class, which represents the Bar Chart visualizing the daily productivity.

"""
from graphics2 import *
from constants import *
from bar import Bar
import pickle


class dailyBarChart:
    def __init__(self, userName, courseToColorDict, week, day, userDataFile): 
        """ 
        Creates a Bar Chart which contains its name, labels for x,y axis, a bar for each course in the courseList and a key which explains what each bar refers to.
        
        """   
        self.name = Text(Point((WINDOW_WIDTH - LEFT_MARGIN)/2 + LEFT_MARGIN, TOP_MARGIN - 100),f"{userName}'s Productivity on {day} - Week {week}") 
        self.name.setSize(25)
        self.xLabel = Text(Point(LEFT_MARGIN, TOP_MARGIN - 35),"Percentage\n" + "of\n" + "completed tasks")
        self.yLabel = Text(Point((WINDOW_WIDTH - LEFT_MARGIN)/2 + LEFT_MARGIN, WINDOW_HEIGHT - 30), "COURSES")
        self.yLabel.setSize(15)
        barWidth = 150 # each bar's width
        
        # calculate the distance for each bar
        if len(courseToColorDict) > 0:
            barDistance = ((WINDOW_WIDTH - LEFT_MARGIN) // len(courseToColorDict)) - barWidth
        xBottomRight = LEFT_MARGIN + barDistance/2 + barWidth # the x coordinate of the bottom right point for the first bar
        
        self.barToCourseName = {} # a dictionary maps a bar to the name of its course 

        # open the userDataFile which contains a dictionary maps a tuple of (week and day) to a list mapping the course to the percent of completed tasks for that course.
        # e.g. { (1, 'Monday') : {'CSC': 80, 'MATH': 50} }
        DayWeekToCoursePercentDict = pickle.load(open(userDataFile,'rb'))
        
        # the Bar Chart key which explains what each bar refers to
        self.key = {} # a dictionary which maps a dot to a course name
        
        y = TOP_MARGIN + 150 # the y coordinate of the center point of the first dot in the key

        for course in courseToColorDict:
            # creates a bar for each course
            percent = DayWeekToCoursePercentDict[(week, day)][course]
            bottomRight = Point(xBottomRight, WINDOW_HEIGHT - BOTTOM_MARGIN)
            bar = Bar(bottomRight, percent, barWidth, course)
            bar.setBarColor(courseToColorDict[course])
            
            courseText = Text(Point(bottomRight.getX() - barWidth/2, bottomRight.getY() + 20), f"{course}")  # a text for the course name at the bottom of a bar
            self.barToCourseName[bar] = courseText
            
            # the x coordinate of the bottom right point for the next bar
            xBottomRight += barDistance + barWidth
            
            # create key for the Bar Chart
            dot = Circle(Point(LEFT_MARGIN/2 - 50,y), 7)
            dot.setFill(courseToColorDict[course])
            dot.setOutline(courseToColorDict[course])
            courseName = Text( Point(LEFT_MARGIN/2 + 20,y),course)
            y += 30
            
            self.key[dot] = courseName
            
        # draw the x and y axis
        self.xAxis = Line(Point(LEFT_MARGIN, TOP_MARGIN), Point(LEFT_MARGIN, WINDOW_HEIGHT - BOTTOM_MARGIN))
        self.yAxis = Line(Point(LEFT_MARGIN, WINDOW_HEIGHT - BOTTOM_MARGIN), Point(WINDOW_WIDTH, WINDOW_HEIGHT - BOTTOM_MARGIN))
        
    
    def draw(self,window):
        """ 
        Draws the Bar Chart on the window.
        
        """ 
        for bar in self.barToCourseName:
            bar.draw(window)
            self.barToCourseName[bar].draw(window)
        
        for dot in self.key:
            dot.draw(window)
            self.key[dot].draw(window)
            
        self.name.draw(window)
        self.xLabel.draw(window)
        self.yLabel.draw(window)
        self.xAxis.draw(window)
        self.yAxis.draw(window)
 







        