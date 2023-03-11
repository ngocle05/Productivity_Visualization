""" 
This module contains the weeklyBarChart class, which represents the Bar Chart visualizing the weekly productivity.

"""
from graphics2 import *
from constants import *
from bar import Bar
import pickle


class weeklyBarChart: 
    def __init__(self, userName, courseToColorDict, week, availableDataDay, userDataFile):
        """ 
        Creates a grouped Bar Chart which contains its name, labels for x,y axis, grouped bars and a key which explains what each bar refers to.
        Bars represents percentage of courses on the same day are grouped together.
        
        """         
        self.name = Text(Point((WINDOW_WIDTH - LEFT_MARGIN)/2 + LEFT_MARGIN, TOP_MARGIN - 100),f"{userName}'s Productivity on Week {week}")
        self.name.setSize(25)
        self.xLabel = Text(Point(LEFT_MARGIN, TOP_MARGIN - 35),"Percentage\n" + "of\n" + "completed tasks") 
        self.yLabel = Text(Point((WINDOW_WIDTH - LEFT_MARGIN)/2 + LEFT_MARGIN, WINDOW_HEIGHT - 30),"COURSES")
        self.yLabel.setSize(15)
        self.groupDistance = 50 # distance between 2 groups of bars
        barDistance = 0 # distance between bars in the same group
        
        barWidth = ((WINDOW_WIDTH - LEFT_MARGIN)// len(availableDataDay) - self.groupDistance) // len(courseToColorDict)
        xBottomRight = LEFT_MARGIN + barDistance/2 + barWidth # the x coordinate of the bottom right point for the first bar
        
        self.dayToBar = {} # a dictionary maps a day to a list of bars representing each course on that day  
        
        # open the userDataFile which contains a dictionary maps a tuple of (week and day) to a list mapping the course to the percent of completed tasks for that course.
        # e.g. { (1, 'Monday') : {'CSC': 80, 'MATH': 50} }
        DayWeekToCoursePercentDict = pickle.load(open(userDataFile,'rb'))
        
        # the Bar Chart key which explains what each bar refers to
        self.key = {} # a dictionary which maps a dot to a course name
        
        y = TOP_MARGIN + 150 # the y coordinate of the center point of the first dot in the key
        
        for course in courseToColorDict:           
            # create key for the Bar Chart
            dot = Circle(Point(LEFT_MARGIN/2 - 50,y), 7)
            dot.setFill(courseToColorDict[course])
            dot.setOutline(courseToColorDict[course])
            courseName = Text( Point(LEFT_MARGIN/2 + 20,y),course)
            y += 30
            
            self.key[dot] = courseName
            
        # creates grouped bars for each day 
        for day in availableDataDay:
            xcenterPoint = xBottomRight + (len(courseToColorDict)*barWidth)/2 - barWidth
            dayText = Text(Point(xcenterPoint, WINDOW_HEIGHT - BOTTOM_MARGIN + 20), f"{day}") # a text for each day at the bottom of each group of bars
            
            self.dayToBar[dayText] = []
        
            # creates a bar for each course on the same day
            for course in courseToColorDict:
                percent = DayWeekToCoursePercentDict[(week, day)][course]
                bottomRight = Point(xBottomRight, WINDOW_HEIGHT - BOTTOM_MARGIN)
                bar = Bar(bottomRight, percent, barWidth, course)
                
                bar.setBarColor(courseToColorDict[course])
                
                if barWidth < 50:
                    bar.setTextSize(barWidth//3) # set size for the percent text

                self.dayToBar[dayText].append(bar)

                # the x coordinate of the bottom right point for the next bar in the same group
                xBottomRight += barDistance + barWidth

                # the x coordinate of the bottom right point for the next bar in a different group
                if course == list(courseToColorDict)[-1]:
                    xBottomRight += self.groupDistance
                    
        
        # draw the x and y axis
        self.xAxis = Line(Point(LEFT_MARGIN, TOP_MARGIN), Point(LEFT_MARGIN, WINDOW_HEIGHT - BOTTOM_MARGIN))
        self.yAxis = Line(Point(LEFT_MARGIN, WINDOW_HEIGHT - BOTTOM_MARGIN), Point(WINDOW_WIDTH, WINDOW_HEIGHT - BOTTOM_MARGIN))
        
    
    def draw(self,window):
        """ 
        Draws the grouped Bar Chart on the window.
        
        """ 
        for day in self.dayToBar:
            day.draw(window)
            for bar in self.dayToBar[day]:
                bar.draw(window)
                
        for dot in self.key:
            dot.draw(window)
            self.key[dot].draw(window)

        self.name.draw(window)
        self.xLabel.draw(window)
        self.yLabel.draw(window)
        self.xAxis.draw(window)
        self.yAxis.draw(window)





        
