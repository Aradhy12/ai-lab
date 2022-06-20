# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from json.encoder import INFINITY
import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(st)
              mdp.getTransitionStatesAndProbs(st, ACT)
              mdp.getReward(st, ACT, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIterations()
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
    def runValueIterations(self):
        States = self.mdp.getStates()#getting the start state
        for iteration in range(self.iterations):#running iteration 
            tempvalues = util.Counter()
            for st in States:
                maxvalue = -INFINITY
                actions = self.mdp.getPossibleActions(st)
                for ACT in actions:
                    transitionStatesProbs = self.mdp.getTransitionStatesAndProbs(st, ACT)
                    sumvalue = 0.0
                    for stateProb in transitionStatesProbs:
                        sumvalue =sumvalue+ stateProb[1] * (self.mdp.getReward(st, ACT, stateProb[0]) + self.discount * self.values[stateProb[0]])    
                    maxvalue = max(maxvalue,sumvalue)
                if maxvalue != -INFINITY:
                    tempvalues[st] = maxvalue
                    
            for st in States:
                self.values[st] = tempvalues[st]

    def getValue(self, st):
        """
          Return the value of the st (computed in __init__).
        """
        return self.values[st]


    def computeQValueFromValues(self, st, ACT):
        """
          Compute the Q-value of ACT in st from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transitionStatesProbs = self.mdp.getTransitionStatesAndProbs(st, ACT)
        val = 0.0
        for stateProb in transitionStatesProbs:
            val =val+ stateProb[1] * (self.mdp.getReward(st, ACT, stateProb[0]) + self.discount * self.values[stateProb[0]]) 
        return val
        #util.raiseNotDefined()

    def computeActionFromValues(self, st):
        """
          The policy is the best ACT in the given st
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal st, you should return None.
        """
        "*** YOUR CODE HERE ***"

        actions = self.mdp.getPossibleActions(st)
        maxact = None
        maxvalueoveractions = -INFINITY
        for ACT in actions: 
           value = self.computeQValueFromValues(st,ACT)
           if value > maxvalueoveractions:
                maxvalueoveractions = value
                maxact = ACT  
        return maxact
        #util.raiseNotDefined()

    def getPolicy(self, st):
        return self.computeActionFromValues(st)

    def getAction(self, st):
        "Returns the policy at the st (no exploration)."
        return self.computeActionFromValues(st)

    def getQValue(self, st, ACT):
        return self.computeQValueFromValues(st, ACT)
