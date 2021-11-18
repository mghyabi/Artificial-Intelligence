# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 19:35:05 2020

@author: mghyabi
"""

import util
import search

Fringe=util.Stack()
Expanded=[]

Start=[search.getStartState(),[]]
Fringe.push(Start)
while not Fringe.isEmpty():
    Move=Fringe.pop()
    if search.problem.isGoalState(Move[0]):
#        return Move[1]
    else:
        for Node in search.problem.getSuccessors(Move[0]):
            if Node[0] not in Expanded:
                Fringe.push([Node[0],Move[1].append(Node[1])])
        Expanded.append(Move[0])



    
