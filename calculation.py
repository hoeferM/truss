#!/usr/bin/python 

import json

with open('data.json', 'r') as file:
    data_str = file.read().replace('\n', '').replace(' ', '')

structur = json.loads(data_str)

class Note(object):


    def __init__(self,data):
        self.fx = 0                          #Supportreaction in X (if Note is Support)
        self.fx_calc = False                 #showes if Forces already calculated
        self.fy = 0                          #Supportreaction in Y (if Note is Support)
        self.fy_calc = False                 #showes if Forces already calculated
        self.fz = 0                          #Supportreaction in Z (if Note is Support)
        self.fz_calc = False                 #showes if Forces already calculated
        self.name = data["name"]
        self.x = data["x"]
        self.y = data["y"]
        self.z = data["z"]
        self.sup = data["s"]        #True if Note is also a Support
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
        self.n1.name = data["n1"]   #First Note of the member
        self.n2.name = data["n2"]   #Second Note of the member


class Force(object):
    def __init__(self,data):
        self.name = data["name"]
        self.note = data["n"]       #Note where the Force is applied
        self.x = data["x"]          #Force in X , Values in N
        self.y = data["y"]          #Force in Y , Values in N
        self.z = data["z"]          #Force in Z , Values in N


def getNote(name):
    for n in notes:
        if (name == n.name):
            return n
    return False

notes = []
members = []
forces = []
for n in structur["notes"]:
    notes.append(Note(n))
#for m in structur["members"]:
#    members.append(Member(m))
#for f in structur["forces"]:
#    forces.append(Force(f))

for n in notes:
    n.show()
