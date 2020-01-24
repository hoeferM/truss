#!/usr/bin/python 
from functions import *
import numpy as np
import mpmath
from sympy import *
from math import pi
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
        self.f_sym = symbols("F_"+ self.name)

    def getN1x(self, nodes):
        return getnodebyName(self.n1, nodes).x

    def getN1y(self, nodes):
        return getnodebyName(self.n1, nodes).y
    
    def getN2x(self, nodes):
        return getnodebyName(self.n2, nodes).x

    def getN2y(self, nodes):
        return getnodebyName(self.n2, nodes).y
    
    def getXEq(self, node, nodes):
        if (node.name == self.n1):
            n2 = getnodebyName(self.n2,nodes)
        else:
            n2 = getnodebyName(self.n1,nodes)
        vec = (node.x - n2.x, node.y - n2.y, node.z - n2.z)
        norm = np.linalg.norm(vec)
        fx = - self.f_sym * vec[0]/norm
        return fx

    def getYEq(self, node, nodes):
        if (node.name == self.n1):
            n2 = getnodebyName(self.n2,nodes)
        else:
            n2 = getnodebyName(self.n1,nodes)
        vec = (node.x - n2.x, node.y - n2.y, node.z - n2.z)
        norm = np.linalg.norm(vec)
        fy = - self.f_sym * vec[1]/norm
        return fy

    def getZEq(self, node, nodes):
        if (node.name == self.n1):
            n2 = getnodebyName(self.n2,nodes)
        else:
            n2 = getnodebyName(self.n1,nodes)
        vec = (node.x - n2.x, node.y - n2.y, node.z - n2.z)
        norm = np.linalg.norm(vec)
        fz = - self.f_sym * vec[2]/norm
        return fz

    def getFkrit(self,nodes):
        L = self.length(nodes)
        I = 0.36           #Moment of inertia of a Spaghetti
        E = 3.5              #Young-Modulo of spaghetti
        return ((4 * pi**2)/L**2) * E * I * 1000

    def getcritMass(self,nodes):
        if(self.f == 0):
            return sym.oo
        elif(self.f > 0):
            return 64.16/(self.f * 9.81)
        else:
            return - self.getFkrit(nodes)/(self.f * 9.81)
    
    def length(self, nodes):
        n1 = getnodebyName(self.n1,nodes) 
        n2 = getnodebyName(self.n2,nodes) 
        vec = (n1.x - n2.x, n1.y - n2.y, n1.z - n2.z)
        return np.linalg.norm(vec)


    def show(self):
        print(self.f_sym)

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

