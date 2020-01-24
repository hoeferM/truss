#!/usr/bin/python 

import json
import mpmath
from sympy import *
from plot import  plot
from models import Node, Member, Force
from functions import *

with open('design2.json', 'r') as file:
    data_str = file.read().replace('\n', '').replace(' ', '')

structur = json.loads(data_str)


#=================INIT

nodes = []
members = []
forces = []
heigth = 0 
widht = 0
for n in structur["nodes"]:         #Load nodes
    nodes.append(Node(n))
for m in structur["members"]:       #Load Members
    members.append(Member(m))
for f in structur["forces"]:        #Load Forces
    forces.append(Force(f))

for n in nodes:
    if ( n.x > widht):
        widht = n.x
    if (n.y > heigth):
        heigth = n.y

heigth += 200
widht += 200

pl = plot(heigth,widht)
pl.nodes(nodes)
pl.members(members, nodes)
for f in forces:
    pl.drawForce(getnodebyName(f.node, nodes), f)
for s in getSup(nodes):
    pl.drawSupport(s)

#=================Program

pl.show()
