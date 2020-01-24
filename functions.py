#!/usr/in/python
import numpy as np
import mpmath
import sympy as sym
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
        #print(xsupports[0].name, xsupports[0].fy)
        #print(lsupports[0].name, lsupports[0].fy)
            
def solveNode(node, mode, nodes,members, forces):
    mem = node.getconnectedMembers(members)
    fx = 0
    fy = 0
    fz = 0
    f = []
    for m in mem:
        fx += m.getXEq(node, nodes)
        fy += m.getYEq(node, nodes)
        fz += m.getZEq(node, nodes)
        f.append(m.f_sym)
    print(fx)
    print(fy)
    print(fz)
    fx = sym.Eq(fx + node.fx, 0)
    fy = sym.Eq(fy + node.fy, 0)
    fz = sym.Eq(fz + node.fz, 0)
    print(fx,fy,fz)
    data = sym.solve((fx,fy,fz))
    print(data)

def solvesystem(nodes, members ,forces):
    equations = []
    variables = []
    for n in nodes:
        mem = n.getconnectedMembers(members)
        fx = 0
        fy = 0
        fz = 0
        symb = []           #list of symbols in the equations
        for m in mem:
            fx += m.getXEq(n, nodes)
            fy += m.getYEq(n, nodes)
            fz += m.getZEq(n, nodes)
            symb.append(m.f_sym)
        for extf in forces:
            if(extf.node == n.name):
                fx += extf.x
                fy += extf.y
                fz += extf.z
        fx = sym.Eq(fx + n.fx, 0)
        fy = sym.Eq(fy + n.fy, 0)
        fz = sym.Eq(fz + n.fz, 0)
        for s in symb:
            variables.append(s)
        equations.append(fx)
        equations.append(fy)
        equations.append(fz)
    variables = tuple(dict.fromkeys(variables))
    equations = tuple(equations)
    solution = sym.solve(equations,variables)
    for m in members:
        if(solution[m.f_sym]):
            m.f = solution[m.f_sym]
            m.fcalc = True
