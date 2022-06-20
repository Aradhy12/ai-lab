# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from __future__ import print_function
from json.tool import main
import queue

from apt import ProblemResolver
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
    
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE "
    #bfs use queue fifo
    stack=util.Stack()
    #stroing state
    state =problem.getStartState()
   
   #pushing stack with a list of action to 
   #be taken and  state
    stack.push((list(),state))
    visited=[]#visited list keep track of visidted state
    while not stack.isEmpty():
         action,currentstate=stack.pop()
         if problem.isGoalState(currentstate):
             return action
         visited.append(currentstate)
         for pos,dir,cost in problem.getSuccessors(currentstate):
           if not pos in visited:
               stack.push((action+[dir],pos))

    

    util.raiseNotDefined()
   

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue=util.Queue()
    #stroing state
    state =problem.getStartState()
   #pushing queue with a list of action to 
   #be taken and  state
    queue.push((list(),state))
    visited=[]#visited list keep track of visidted state
    while not queue.isEmpty():
         action,currentstate=queue.pop()
         if problem.isGoalState(currentstate):
             return action
         visited.append(currentstate)
         for pos,dir,cost in problem.getSuccessors(currentstate):
           if not pos in visited:
               queue.push((action+[dir],pos))
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
   
    pqueue = util.PriorityQueue()
    state = problem.getStartState()
    par={}#a dictionary with state as key and value as parent of currnet state

 
    cost={}#a dictionary with state as key and value as pathcost from start to  currnet state
     
    visited={}#a dictionary with state as key and value containing a tuple of the form (parent of this atate,action from parent to this state)
    act={}#a dictionary with state as key and value as action to reach the current state from start
    pqueue.update(state, 0)
 
    par[state]=(None)
    act[state]=(None)
    cost[state]=(0)
    
    while not pqueue.isEmpty():
        current_state = pqueue.pop()
        parent=par[current_state]
        action=act[current_state]
        pcost=cost[current_state]
        
        #If goal state is found then back trace it using the stored parent to get the list of actions
        if problem.isGoalState(current_state):
            path=[]
            while parent!=None:
                path.append(action)
                (p,action)=visited[parent]
                parent=p
            path.reverse()
            return path
    
        visited[current_state]=(par.pop(current_state),act.pop(current_state))

        for pos, dir, step in problem.getSuccessors(current_state):
            pathcost=pcost+step
            if pos not in visited:
                pqueue.update(pos,pathcost)
                par[pos]=current_state
                act[pos]=dir
                cost[pos]=pathcost
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pqueue = util.PriorityQueue()#PriorityQueue with path cost as it Priority
    state = problem.getStartState()
    par={}#a dictionary with state as key and value as parent of currnet state

 
    cost={}#a dictionary with state as key and value as pathcost from start to  currnet state
     
    visited={}#a dictionary with state as key and value containing a tuple of the form (parent of this atate,action from parent to this state)
    act={}#a dictionary with state as key and value as action to reach the current state from start
    pqueue.update(state,heuristic(state,problem))
 
    par[state]=(None)
    act[state]=(None)
    cost[state]=heuristic(state,problem)
    
    while not pqueue.isEmpty():
        current_state = pqueue.pop()
        parent=par[current_state]
        action=act[current_state]
        pcost=cost[current_state]
        
        #If goal state is found then back trace it using the stored parent to get the list of actions
        if problem.isGoalState(current_state):
            path=[]
            while parent!=None:
                path.append(action)
                (p,action)=visited[parent]
                parent=p
            path.reverse()
            return path
    
        visited[current_state]=(par.pop(current_state),act.pop(current_state))

        for pos, dir, step in problem.getSuccessors(current_state):
            pathcost=pcost+step+heuristic(pos,problem)-heuristic(current_state,problem)
            if pos not in visited:
                pqueue.update(pos,pathcost)
                par[pos]=current_state
                act[pos]=dir
                cost[pos]=pathcost



    util.raiseNotDefined()
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
