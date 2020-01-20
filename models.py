#!/usr/bin/python 
from functions import *
import mpmath
from sympy import *

#=================Class Definitions

class Node(object):


    def __init__(self,data):
        self.fx = 0                          #Supportreaction in X (if node is Support)
        self.fx_calc = False                 #showes if Forces already calculated
        self.fy = 0                          #Supportreaction in Y (if node is Support)
        self.fy_calc = False                 #showes if Forces already calculated
        self.fz = 0                          #Supportreaction in Z (if node is Support)
        self.fz_calc = False                 #showes if Forces already calculated
        self.name = data["name"]
        self.x = data["x"]
        self.y = data["y"]
        self.z = data["z"]
        self.sup = data["s"]        #True if node is also a Support
        self.x_fixed = data["xf"]   #If Support and Fixed in X direction
        self.z_fixed = data["zf"]   #If Support and Fixed in Z direction
        if (not self.sup):
            self.fx_calc = True
            self.fy_calc = True
            self.fz_calc = True
        else:
            if (not self.x_fixed):
                self.fx_calc = True
            if (not self.z_fixed):
                self.fz_calc = True


    def openReactions(self):
        i = 0
        if (not self.fx_calc):
            i += 1
        if (not self.fy_calc):
            i += 1
        if (not self.fz_calc):
            i += 1
        return i

    def getconnectedMembers(self, members):
        connented = []
        for m in members:
            if (m.n1 == self.name or m.n2 == self.name ):
                connented.append(m)
        return connented
    
    def unknownForces(self, members):       #retruns the number of unknown Forces
        i = 0
        members = self.getconnectedMembers(members)
        for m in members:
            if (not m.fcalc):
                i += 1
        return i

    def show(self):
        print("======================================================")
        print("Node Print:")
        print("Name: "+ self.name) 
        print("X: "+ str(self.x))
        print("Y: "+ str(self.y)) 
        print("Z: "+ str(self.z)) 
        print("Support: "+ str(self.sup)) 
        print("Fixed in X: "+ str(self.x_fixed)) 
        print("Fixed in Z: "+ str(self.z_fixed))
        print("Reaction in X: "+ str(self.fx)) 
        print("Reaction in Y: "+ str(self.fy)) 
        print("Reaction in Z: "+ str(self.fz)) 
        print("Reaction X Calculated: "+ str(self.fx_calc))
        print("Reaction Y Calculated: "+ str(self.fy_calc)) 
        print("Reaction Z Calculated: "+ str(self.fz_calc)) 

class Member(object):
    def __init__(self,data):
        self.name = data["name"]
        self.n1 = data["n1"]   #First node of the member
        self.n2 = data["n2"]   #Second node of the member
        #Forces that are at the ends of the member
        self.f = 0
        self.fcalc = False


    def getN1x(self, nodes):
        return getnodebyName(self.n1, nodes).x

    def getN1y(self, nodes):
        return getnodebyName(self.n1, nodes).y
    
    def getN2x(self, nodes):
        return getnodebyName(self.n2, nodes).x

    def getN2y(self, nodes):
        return getnodebyName(self.n2, nodes).y
    

    def show(self):
        print(self.fx_n1_sym, self.fx_n1_cal)
        print(self.fx_n2_sym, self.fx_n2_cal)
        print(self.fy_n1_sym, self.fy_n1_cal)
        print(self.fy_n2_sym, self.fy_n2_cal)
        print(self.fz_n1_sym, self.fz_n1_cal)
        print(self.fz_n2_sym, self.fz_n2_cal)

class Force(object):
    def __init__(self,data):
        self.name = data["name"]
        self.sym = symbols(data["name"])     
        self.node = data["n"]       #node where the Force is applied
        self.x = data["x"]          #Force in X , Values in N
        self.y = data["y"]          #Force in Y , Values in N
        self.z = data["z"]          #Force in Z , Values in N

    def getNodeX(self, nodes):
        return getnodebyName(self.node , nodes).x

    def getNodeY(self, nodes):
        return getnodebyName(self.node , nodes).y

    def getNodeZ(self, nodes):
        return getnodebyName(self.node , nodes).z
    
    def show(self):
        print(type(self.sym))
        print(self.sym)

