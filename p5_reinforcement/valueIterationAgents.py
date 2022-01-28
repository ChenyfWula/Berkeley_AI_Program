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


from typing import NamedTuple
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
        for iteration in range(self.iterations):
            value_copy = self.values.copy()
            states = self.mdp.getStates()
            
            for state in states:
                if self.mdp.isTerminal(state):
                    value_copy[state] = 0
                else:
                    action = self.computeActionFromValues(state)
                    Q_value = self.computeQValueFromValues(state,action)
                    value_copy[state] = Q_value
            
            self.values = value_copy


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
        
        T_sas_list = self.mdp.getTransitionStatesAndProbs(state, action)
        Q_value = 0
        for item in T_sas_list:
            nextState, T_sas = item

            R_sas = self.mdp.getReward(state,action,nextState)
            Q_value += T_sas*(R_sas+self.discount*self.getValue(nextState))
        
        return Q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        '''Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)'''
        
        PossibleActions = self.mdp.getPossibleActions(state)
        
        if (len(PossibleActions) == 0):
            return None
        
        Q_dict = {}
        for action in PossibleActions:
            Q_value = self.computeQValueFromValues(state,action)
            Q_dict[Q_value] = action
        return Q_dict[max(Q_dict.keys())]
        #util.raiseNotDefined()

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
        states = self.mdp.getStates()
        state_num = len(states)
        for cnt in range(self.iterations):
            state = states[cnt % state_num]
            if self.mdp.isTerminal(state):
                continue
            action = self.computeActionFromValues(state)
            Q_value = self.computeQValueFromValues(state,action)
            self.values[state] = Q_value

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
        #Compute predecessors of all states.
        predecessor_dict = {}
        states = self.mdp.getStates()
        for state in states:
            predecessor_dict[state] = self.getPredecessors(state)
        
        #Initialize an empty priority queue.
        min_heap = util.PriorityQueue()
        
        #min_heap initialize
        for state in states:
            if not self.mdp.isTerminal(state):
                #Find the absolute value
                action = self.computeActionFromValues(state)
                Q_value = self.computeQValueFromValues(state,action)
                diff = abs(self.getValue(state)-Q_value)
                #Push s into the priority queue with priority -diff
                min_heap.push(state,-diff)
        
        for cnt in range(self.iterations):
            #If the priority queue is empty, then terminate.
            if min_heap.isEmpty():
                break
            max_error_state = min_heap.pop()
            #Update the value of s (if it is not a terminal state) in self.values
            action = self.computeActionFromValues(max_error_state)
            self.values[max_error_state] = self.computeQValueFromValues(max_error_state,action)
            
            #For each predecessor p of s, do:
            for p in predecessor_dict[max_error_state]:
                #find diff
                action = self.computeActionFromValues(p)
                Q_value = self.computeQValueFromValues(p,action)
                diff = abs(self.getValue(p)-Q_value)
                
                if diff > self.theta:
                    min_heap.update(p,-diff)
                
            
        
        
    def getPredecessors(self,state):
        predecessor_set = set()
        states = self.mdp.getStates()
        
        if self.mdp.isTerminal(state):
            return
        else:
            for p_state in states:
                if self.mdp.isTerminal(p_state):
                    continue
                possible_action = self.mdp.getPossibleActions(p_state)
                for action in possible_action:
                    T_sas_list = self.mdp.getTransitionStatesAndProbs(p_state, action)
                    
                    for T_state, T_sas in T_sas_list:
                        if (T_state == state) and (T_sas> 0):
                            predecessor_set.add(p_state)
            return predecessor_set
            

