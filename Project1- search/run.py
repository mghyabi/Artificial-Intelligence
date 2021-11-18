# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 15:36:50 2020

@author: mghyabi
"""

# Question 1
#runfile('pacman.py',args='-l bigMaze -z 0.5 -p SearchAgent')

# Question 2
#runfile('pacman.py',args=' -l bigMaze -p SearchAgent -a fn=bfs -z .5')
#runfile('eightpuzzle.py')

# Question 3
#runfile('pacman.py',args='-l bigMaze -p SearchAgent -a fn=ucs -z 0.5')

# Question 4
#runfile('pacman.py',args='-l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic')

# Question 5
runfile('pacman.py',args='-l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem -z 0.5')

# Question 6
#runfile('pacman.py',args='-p SearchAgent -a fn=aStarSearch,prob=CornersProblem,heuristic=cornersHeuristic -z 0.5')

# Question 7
#runfile('pacman.py',args='-l trickySearch -p AStarFoodSearchAgent ')

# Question 8
#runfile('pacman.py',args='-l bigSearch -p ClosestDotSearchAgent -z .5 ')



