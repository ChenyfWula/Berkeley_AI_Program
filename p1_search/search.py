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

import util
import copy
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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("I    s the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    Expanded = []
    child_dict = {}

    import util
    frontier = util.Stack()
    frontier.push(problem.getStartState())

    while not frontier.isEmpty():
        node = frontier.pop()

        if problem.isGoalState(node):
            Expanded.append(node)
            break

        if node not in Expanded:
            Expanded.append(node)
            children = problem.getSuccessors(node)
            child_dict[str(node)] = children
            
            for item in children:
                if item[0] not in Expanded:
                    frontier.push(item[0])

    path = []
    node = Expanded[len(Expanded)-1]
    for i in range(2,len(Expanded)+1):
        for child in child_dict[str(Expanded[len(Expanded)-i])]:
            if child[0] == node:
                path.insert(0,child[1])
                node = Expanded[len(Expanded)-i]

    return path


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    Expanded = []
    Expanded_path = {}
    path = []
    frontier = util.Queue()

    node = problem.getStartState()
    Expanded.append(node)
    children = problem.getSuccessors(node)

    for child in children:
        if child[0] not in Expanded:
            Expanded_path[str((child[0],child[1]))] = [child[1]]
            frontier.push(list(child))

    while not frontier.isEmpty():
        node = frontier.pop()

        if problem.isGoalState(node[0]):
            Expanded.append(node[0])
            path = Expanded_path[str((node[0],node[1]))]
            break

        if node[0] not in Expanded:
            Expanded.append(node[0])
            children = problem.getSuccessors(node[0])
                     
            for child in children:                
                if child[0] not in Expanded:   
                    Expanded_path[str((child[0],child[1]))] = copy.deepcopy(Expanded_path[str((node[0],node[1]))])
                    Expanded_path[str((child[0],child[1]))].append(child[1])
                    child = list(child)                   
                    frontier.push(child)

    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    Expanded = []
    Expanded_path = {}
    path = []
    frontier = util.PriorityQueue()

    node = problem.getStartState()
    Expanded.append(node)
    children = problem.getSuccessors(node)

    for child in children:
        if child[0] not in Expanded:
            Expanded_path[str((child[0],child[1]))] = [child[1]]
            frontier.push(list(child),child[2])

    while not frontier.isEmpty():
        node = frontier.pop()

        if problem.isGoalState(node[0]):
            Expanded.append(node[0])
            path = Expanded_path[str((node[0],node[1]))]
            break

        if node[0] not in Expanded:
            Expanded.append(node[0])
            children = problem.getSuccessors(node[0])
                     
            for child in children:                
                if child[0] not in Expanded:   
                    Expanded_path[str((child[0],child[1]))] = copy.deepcopy(Expanded_path[str((node[0],node[1]))])
                    Expanded_path[str((child[0],child[1]))].append(child[1])
                    child = list(child)                   
                    child[2] = child[2] + node[2]
                    frontier.push(child,child[2])


    return path
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    Expanded = []
    Expanded_path = {}
    path = []
    frontier = util.PriorityQueue()

    node = problem.getStartState()
    Expanded.append(node)
    children = problem.getSuccessors(node)


    for child in children:
        # import pdb
        # pdb.set_trace()
        if child[0] not in Expanded:
            Expanded_path[str((child[0],child[1]))] = [child[1]]
            child = list(child)
            child[2] = child[2] +  heuristic(child[0],problem) 
            frontier.push(child,child[2])

    # import pdb
    # pdb.set_trace()
    while not frontier.isEmpty():
        # import pdb
        # pdb.set_trace()
        node = frontier.pop() #accumlated node value
        Covered_distance = node[2] - heuristic(node[0],problem)
        if problem.isGoalState(node[0]):
            Expanded.append(node[0])
            path = Expanded_path[str((node[0],node[1]))]
            break

        if node[0] not in Expanded:
            Expanded.append(node[0])
            children = problem.getSuccessors(node[0])
                     
            for child in children:                
                if child[0] not in Expanded:   
                    Expanded_path[str((child[0],child[1]))] = copy.deepcopy(Expanded_path[str((node[0],node[1]))])
                    Expanded_path[str((child[0],child[1]))].append(child[1])
                    child = list(child)                   
                    child[2] = child[2] + Covered_distance + heuristic(child[0],problem)
                    frontier.push(child,child[2])


    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
