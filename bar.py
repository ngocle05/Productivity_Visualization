""" 
This module contains the Bar class which represents a bar with its percent inside it.

"""
from graphics2 import *
from constants import *

class Bar:
    def __init__(self, bottomRight, percent, barWidth, courseName): 
        """ 
        Creates a bar at a given current point with its percent inside it.

        """
        self.color = "light green" 
        self.percent = percent
        self.height = (self.percent * MAX_BAR_HEIGHT)/100
        self.width = barWidth
        
        topLeft = Point(bottomRight.getX() - self.width, bottomRight.getY() - self.height)
        self.bar = Rectangle(topLeft, bottomRight)
        self.text = Text(Point(topLeft.getX() + self.width/2, topLeft.getY() + self.height/2), f"{self.percent}")
        
    def setBarColor(self,color):
        """Set size for a bar"""
        self.color = color
    
    def setTextSize(self,sizeNum):
        """Set size for self.text"""
        self.text.setSize(sizeNum)
        
    
    def draw(self, win):
        """Draws the progress bar on the window"""
        self.bar.draw(win)
        self.bar.setFill(self.color)
        if self.percent > 0:
            self.text.draw(win)
            

        
        
        
        