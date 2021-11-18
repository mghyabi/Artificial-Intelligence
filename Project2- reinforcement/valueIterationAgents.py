# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

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
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        #initiate 0 value for all states
        for s in self.mdp.getStates():
            self.values[s] = 0
        #main loop    
        for i in range(self.iterations):
            #implementng batch value iteration
            batchValues = self.values.copy()
            #looping over all states
            for s in self.mdp.getStates():
                #counter to store Qvalues
                sValues = util.Counter()
                #looping over possible actions from each state
                for a in self.mdp.getPossibleActions(s):
                    sValues[a] = self.getQValue(s,a)
                #Max over a in each state
                batchValues[s] = sValues[sValues.argMax()]
            
            #assigning new values to each state
            self.values = batchValues.copy()



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        
        Qvalue = 0
        for move in self.mdp.getTransitionStatesAndProbs(state,action):
            #weighted average over s_prime, of reward from possible resulting actions 
            Qvalue += move[1]*(self.mdp.getReward(state,action,move[0])+self.discount*self.getValue(move[0]))

        return Qvalue
        
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        if (self.mdp.isTerminal(state)):
            return None
        else:
            Qvalues = util.Counter()
            for a in self.mdp.getPossibleActions(state):
                #enumerating Q for different possible acctions
                Qvalues[a] = self.computeQValueFromValues(state,a)

            bestAction = Qvalues.argMax()
            
            return bestAction
        
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        
        Iteration = 0

        while Iteration < self.iterations:
            #looping over states until iteration cap reached
          for s in self.mdp.getStates():
            #setting up a new QValue for each state
            QValues = util.Counter() 
            
            #enumerating Qvalues in each state according to possible actions from it
            for a in self.mdp.getPossibleActions(s):
              QValues[a] = self.computeQValueFromValues(s,a)
            
            #max over actions in each state
            self.values[s] = QValues[QValues.argMax()]
            
            Iteration += 1
            if Iteration >= self.iterations:
              return
        return

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        
        Queue = util.PriorityQueue()

        Predecessors={}
        
        #looping over all states to find connections between states
        for s in self.mdp.getStates():
            #acting on non-terminal states
            if not self.mdp.isTerminal(s):
                for a in self.mdp.getPossibleActions(s):
                    for sPrime,_ in self.mdp.getTransitionStatesAndProbs(s,a):
                        if sPrime in Predecessors:
                            Predecessors[sPrime].add(s)
                        else:
                            Predecessors[sPrime]={s}


        for s in self.mdp.getStates():
            if not self.mdp.isTerminal(s):
                Queue.update(s, -abs(self.values[s] - max([self.computeQValueFromValues(s,a) for a in self.mdp.getPossibleActions(s)])))

        for i in range(self.iterations):
            if  not Queue.isEmpty():
                s = Queue.pop()
                if not self.mdp.isTerminal(s):
                    self.values[s] = max([self.computeQValueFromValues(s,a) for a in self.mdp.getPossibleActions(s)])
    
                for p in Predecessors[s]:
                    if not self.mdp.isTerminal(p):
                        ValueDifference = abs(self.values[p] - max([self.computeQValueFromValues(p,a) for a in self.mdp.getPossibleActions(p)]))
                        if self.theta < ValueDifference:
                                Queue.update(p,-ValueDifference)