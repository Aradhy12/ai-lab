# by 112001006 and 112001024
# multiAgents.py
#
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]
    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #List of positions of the food.
        foodList=newFood.asList()
        #Sum of manhattan distance of all food
        sum=0
        if successorGameState.isWin():
            return 999999
        
        #this return  high negative if ghost is very close.
        for ghoststate in newGhostStates:
            xy1=ghoststate.getPosition()
            xy2=newPos
            #calculating mahantann distance
            if abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])<=1:
                return -9999999
    
        #this prevent pacman from making none moves
        if currentGameState.getPacmanPosition() == newPos:
            return -9999999
        


        #calculating sum of manhattan distance for all food
        for i in foodList:
            sum+=abs(i[0] - newPos[0]) + abs(i[1] - newPos[1])
        #If all foods are taken we return very high utility.

        if len(foodList)!=0:
            final=3500/sum + 25000/len(foodList)
        else:
            return 99999999



        return final
   

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1


        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game
        gameState.isWin():
        Returns whether or not the game state is a winning state
        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        

    
         #Total agents in the game
        agent=gameState.getNumAgents()
        #Number of ghost in the pacman game

        ghost=agent-1

        ans=self.minmax(gameState,self.depth,ghost)
        #rreturn the the direction to move
        return ans
    
    def minmax(self,state,d,a):
        #get all  the legal action
        legalMoves=state.getLegalActions(0)
        #calling mini function and storing all it's value in arr
        arr=[self.mini(state.generateSuccessor(0, action),d,a,1) for action in legalMoves]
        m=max(arr)

      #choose one of the best action
        bestIndices = [index for index in range(len(arr)) if arr[index] == m]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]
    
    #return max utility for all successor state

    def maxi(self,state,d,a):
        #return ecaluaton function if dept had been reached
        if(d==0):
            return self.evaluationFunction(state)

        legalMoves=state.getLegalActions(0)
        #calling for it children mini func recursively
        arr=[self.mini(state.generateSuccessor(0, action),d,a,1) for action in legalMoves]
        #if Arr is empty mean no succsecor return a evalaution function
        if(arr==[]):
            return self.evaluationFunction(state)


        # returns max of all utilities values of it 's successors as max function
        return max(arr)
    
    #Funtion to select move for ghosts. Min utility among all successor states
    def mini(self,state,d,a,b):
        #only goes to max function when we have evalated for all min agents
        if(a==1):
            legalMoves=state.getLegalActions(b)
            arr=[self.maxi(state.generateSuccessor(b, action),d-1,b) for action in legalMoves]
             #if Arr is empty mean no succsecor return a evalaution function
          
            if(arr==[]):
                return self.evaluationFunction(state)

            #Return min of all utility values of its successors
            return min(arr)
        else:
            legalMoves=state.getLegalActions(b)
            arr=[self.mini(state.generateSuccessor(b, action),d,a-1,b+1) for action in legalMoves]
            #If no successors return evaluation value
         
            if(arr==[]):
                return self.evaluationFunction(state)
            #return min of all utility values of its successors
            return min(arr)



        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

       
        
        agent=gameState.getNumAgents()
        #number of ghost in pacman
        ghost=agent-1
        ans=self.alphabeta(gameState,self.depth,ghost,-9999999,+99999999)
        return ans
    #alpha beta pruning
    def alphabeta(self,state,d,a,alpha,beta):
        legalMoves=state.getLegalActions(0)

        v=-9999999999
        for action in legalMoves:
             #Since next level is Min, calling Min for successors
            x=self.mini(state.generateSuccessor(0, action),d,a,1,alpha,beta)
             #Choosing the Action which is Max of Successor
            if x>=v:
                v=x
                maxval=action
             #Updating alpha value at root
            if v<beta:
                alpha=max(alpha,v)
        return maxval
    
    #max ulility function for pacman return the max ultility
    def maxi(self,state,d,a,alpha,beta):
        legalmoves=state.getLegalActions(0)
       #returning if their is no successor

        if(legalmoves==[]):
            return self.evaluationFunction(state)
        if(d==0):
            return self.evaluationFunction(state)
        t=-9999999999
        #for each action returning max among all successors
        for action in legalmoves:
            t=max(t,self.mini(state.generateSuccessor(0, action),d,a,1,alpha,beta))
            if t<=beta:
                alpha=max(alpha,t)
            else: return t#run till the  expected range is range (alpha,beta) 0
        return t

    def mini(self,state,d,a,b,alpha,beta):
        #if utility of all ghost is completed 
       #than goes to max
         if(a==1):
            legalmoves=state.getLegalActions(b)
            #if no sucesor  return the evalution function
            if(legalmoves==[]):
                   return self.evaluationFunction(state)
            v=9999999999
            #if expected range is alha to beta than(return the min value)
            for action in legalmoves:
                 v=min(v,self.maxi(state.generateSuccessor(b, action),d-1,b,alpha,beta))
                 if v>=alpha:
                        beta=min(beta,v)
                 else:   return v
            return v
         else:

            legalmoves=state.getLegalActions(b)
            if(legalmoves==[]):
                return self.evaluationFunction(state)
                   #if expected range is alha to beta than(return the min value)
            v=9999999999
            for action in legalmoves:
                v=min(v,self.mini(state.generateSuccessor(b, action),d,a-1,b+1,alpha,beta))
                if v>=alpha:
                      beta=min(beta,v)
                else: return v
            return v


    
    
         util.raiseNotDefined()




class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"  
        #Total agents in the game
        agents=gameState.getNumAgents()
        #Number of ghosts
        ghost=agents-1
        ans=self.expecti(gameState,self.depth,ghost)
        return ans
    
    def expecti(self,state,d,a):
       
        legalmoves=state.getLegalActions(0)
        arr=[self.mini(state.generateSuccessor(0, action),d,a,1) for action in legalmoves]
       
        ma=max(arr)
        bestIndices = [index for index in range(len(arr)) if arr[index] == ma]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalmoves[chosenIndex]
    
    #this function select the move for the pacman
    #give the max utility among all succesor state
    def maxi(self,state,d,a):
        if(d==0):
            return self.evaluationFunction(state)#retrun if dept is reached
        legalMoves=state.getLegalActions(0)#getting all legal action of pacman
        
        arr=[self.mini(state.generateSuccessor(0, action),d,a,1) for action in legalMoves]
        #no succesor
        if(arr==[]):
            return self.evaluationFunction(state)
        sum=0.0
        return max(arr)
    #select minium utility among all move's
    def mini(self,state,d,a,b):
        #only goes to max if  all ghost had calculated the values
        if(a!=1):
            legalMoves=state.getLegalActions(b)
            arr=[self.mini(state.generateSuccessor(b, action),d,a-1,b+1) for action in legalMoves]
        
            if(arr==[]):
                return self.evaluationFunction(state)
            sum=0.0
            for x in arr:
                sum+=x
            return float(float(sum)/float(len(arr)))
       
        else:
            
            legalMoves=state.getLegalActions(b)
            arr=[self.maxi(state.generateSuccessor(b, action),d-1,b) for action in legalMoves]
            if(arr==[]):
                return self.evaluationFunction(state)

            sum=0.0
            #returning avg value -as treated equaly likely
            #as ghost play random moves
            for x in arr:
                sum+=x
            return float(float(sum)/float(len(arr)))

       
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    "*** YOUR CODE HERE ***"
    

    #List of coordinates of all food particles
    foodList=newFood.asList()
    #sum of manhattan distance of all food particles
    sum=0
    #tells if ghost is at a manhattan distance greater than 4 units
    far=0
    
    for ghoststate in newGhostStates:
        x1=ghoststate.getPosition()
        x2=newPos
        if abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])<=2:
            return -99999999#only give high negative value when the ghost is too far
       

        elif abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])>=4:
            far=1

    x=0#for storing manhantan dis for ghost
    if len(newScaredTimes)>0:
        x1=ghoststate.getPosition()
        x2=newPos
        x=abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])
        
    
    #calculationg mahattan distamce for all food
    for i in foodList:
        x1=i
        x2=newPos
        sum+=abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])
#dont include sum if ghostis too far away
    if len(foodList)==0:
        return 99999999
    final = 31000/len(foodList)
    if far==1:
        final+=3500/x
    else:
         if len(newScaredTimes)>0:
             final+=3000/x+4500/sum
         else:
             final+=4500/sum
        

    return final


# Abbreviation
better = betterEvaluationFunction