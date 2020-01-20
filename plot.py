import cv2
import numpy as np
import math
from functions import *

class plot():

    def __init__(self,height, width):
        self.height = height
        self.width = width
        self.img = np.zeros((height,width,3), np.uint8)
        self.img[:,:] = (255,255,255)

    def nodes(self, nodes):
        for n in nodes:
            cv2.circle(self.img, (n.x + 100, self.height - 100 - n.y), 2, (255,0,0), 2)

    def members(self, member, nodes):
        for m in member:
            x1 = self.getX(m.getN1x(nodes))
            y1 = self.getY(m.getN1y(nodes))
            x2 = self.getX(m.getN2x(nodes))
            y2 = self.getY(m.getN2y(nodes))
            cv2.line(self.img, (x1,y1),(x2,y2),(0,0,0),1)
   
    def getX(self, xcordinate):
        return xcordinate + 100

    def getY(self, ycordinate):
        return self.height -100 - ycordinate

    def drawIntForce(self, node , direct, magnitude):       #Draw internal Forces
        x2 = self.getX(node.x)
        y2 = self.getY(node.y)
        if (direct == "x"):
            y1 = y2
            x1 = x2 - magnitude
        if (direct == "y"):
            x1 = x2
            y1 = y2 - magnitude
        start = (x1,y1)
        end = (x2,y2)
        self.img = cv2.arrowedLine(self.img,start,end,(0,0,255),2)

    def drawForce(self, node, force):
        x1 = self.getX(node.x)
        y1 = self.getY(node.y)
        x2 = -int(force.x / 2) + x1
        y2 = -int(force.y / 2) + y1
        magnitude = str(math.sqrt(force.x ** 2 + force.y ** 2))+" N"
        start = (x1,y1)
        end = (x2,y2)
        self.img = cv2.arrowedLine(self.img,start,end,(0,0,255),2)
        self.img = cv2.putText(self.img,magnitude, (x1 + 5 ,y1 + 20 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

    def drawSupport(self, node):
        x1 = self.getX(node.x)
        y1 = self.getY(node.y)
        pt1 = (x1,y1)
        pt2 = (x1 - 10, y1 + 20)
        pt3 = (x1 + 10, y1 + 20)
        
        cv2.circle(self.img, pt1, 0, (0,0,0), -1)
        cv2.circle(self.img, pt2, 0, (0,0,0), -1)
        cv2.circle(self.img, pt3, 0, (0,0,0), -1)
        triangle_cnt = np.array( [pt1, pt2, pt3] )
        
        cv2.drawContours(self.img, [triangle_cnt], 0, (0,0,0), -1)

    def drawSupportForces2D(self, nodes):
        sx = getSupfx(nodes)
        sy = getSup(nodes)
        for x in sx:
            x1 = self.getX(x.x)
            y1 = self.getY(x.y)
            start = (x1 - 40, y1)
            end = (x1 - 3,y1)
            magnitude = str(x.fx)+" N"
            self.img = cv2.arrowedLine(self.img,start,end,(0,0,255),2)
            self.img = cv2.putText(self.img,magnitude, (x1 - 30 ,y1 - 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        for y in sy:
            x1 = self.getX(y.x)
            y1 = self.getY(y.y)
            start = (x1, y1 + 40)
            end = (x1 ,y1 + 3)
            magnitude = str(y.fy)+" N"
            self.img = cv2.arrowedLine(self.img,start,end,(0,0,255),2)
            self.img = cv2.putText(self.img,magnitude, (x1 + 15 ,y1 + 30 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        

    def show(self):
        cv2.imshow("Bridge plot", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
