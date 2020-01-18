#!/usr/bin/python 
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
    if (len(getSupfx(nodes)) == 1):
        f = 0 
        for i in forces:
            f += i.x
        getSupfx(nodes).fx = - f
        getSupfx(nodes).fx_calc = - f
        
        
    pass

