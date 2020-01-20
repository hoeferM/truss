#!/usr/in/python
import numpy as np

#=================Function Definitions


def getnodebyName(name, nodes):
    for n in nodes:
        if (name == n.name):
            return n
    return False


def getSup(nodes):
    supp = []
    for n in nodes:
        if (n.sup):
            supp.append(n)
    return supp

def getSupfx(nodes):         #retruns array of the names of supports that are fixed in x Direction
    supp = []
    for n in nodes:
        if (n.sup and n.x_fixed):
            supp.append(n)
    return supp

def getSupfz(nodes):         #retruns array of the names of supports that are fixed in z Direction

    supp = []
    for n in nodes:
        if (n.sup and n.z_fixed):
            supp.append(n)
    return supp

def getSupl(nodes):         #retruns array of loose supports (exept for y - Direction
    supp = []
    for n in nodes:
        if (n.sup and not n.x_fixed and not n.z_fixed):
            supp.append(n)
    return supp

def getMode(nodes, structur):          #returns if 2D or 3D mode or if error with teh number of supports
    if(structur['mode'] == "2D" and 
            len(getSup(nodes)) == 2 and 
            len(getSupfx(nodes)) == 1 and 
            len(getSupfz(nodes)) == 1):
        return 2
    elif(structur['mode'] == "3D" and 
            len(getSup(nodes)) == 4 and 
            len(getSupfx(nodes)) == 2 and 
            len(getSupfz(nodes)) == 1):
        return 3
    else:
        return 0

def setMode(m, nod, mem):
    if(m == 2):
        for n in nod:
            n.fz_calc = True
        for m in mem:
            m.fz_n1_cal = True
            m.fz_n2_cal = True

       

def statDefined(m, nodes,mem):
    f = 1
    if (m == 2):
        #f = 2 * number of nodeses - ( number of reaction forces + number of members )
        f = 2 * len(nodes) - ( len(getSup(nodes)) + len(getSupfx(nodes)) + len(mem))
    if (m == 3):
        #f = 3 * number of nodeses - ( number of reaction forces + number of members )
        f = 3 * len(nodes) - ( len(getSup(nodes)) + len(getSupfx(nodes)) + len(mem))
    return f

def supportReactions(mode, nodes, members, forces):
    supports = getSup(nodes)
    xsupports = getSupfx(nodes)
    lsupports = getSupl(nodes)
    sum_fy = 0
    if (len(xsupports) == 1):
        f = 0
        for i in forces:
            f += i.x
        getSupfx(nodes)[0].fx = - f
        getSupfx(nodes)[0].fx_calc = True
    else:
        print("To many fixed supports in x-Direction")
        return False
    if (len(supports) == 2):
        
        x1 = xsupports[0].x
        y1 = xsupports[0].y
        x2 = lsupports[0].x
        y2 = lsupports[0].y
        s1 = [x1,y1]
        s2 = [x2,y2]
        mom_f = 0
        for f in forces:
            dist = (f.getNodeX(nodes) - x1,f.getNodeY(nodes) - y1)
            f_vect = (f.x, f.y)
            mom_f += np.cross(dist, f_vect)
            sum_fy += f.y
        lsupports[0].fy = - (1 / (x2 - x1)) * mom_f
        lsupports[0].fy_calc = True
        
        xsupports[0].fy = - sum_fy - lsupports[0].fy
        print(xsupports[0].name, xsupports[0].fy)
        print(lsupports[0].name, lsupports[0].fy)
            

