import cv2
import numpy as np

class plot():

    def __init__(self,height, width):
        self.height = height
        self.width = width
        self.img = np.zeros((height,width,3), np.uint8)
        self.img[:,:] = (255,255,255)

    def nodes(self, nodes):
        for n in nodes:
            cv2.circle(self.img, (self.width - 100 - n.x, self.height - 100 - n.y), 2, (255,0,0), 2)

    def members(self, member, nodes):
        for m in member:
            x1 = self.getX(m.getN1x(nodes))
            y1 = self.getY(m.getN1y(nodes))
            x2 = self.getX(m.getN2x(nodes))
            y2 = self.getY(m.getN2y(nodes))
            cv2.line(self.img, (x1,y1),(x2,y2),(0,0,0),1)
   
    def getX(self, xcordinate):
        return self.width -100 - xcordinate

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
        x2 = -int(force.x) + x1
        y2 = -int(force.y) + y1
        print(x1,y1,x2,y2)
        print(force.y)
        start = (x1,y1)
        end = (x2,y2)
        self.img = cv2.arrowedLine(self.img,start,end,(0,0,255),2)



    def show(self):
        cv2.imshow("Bridge plot", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
