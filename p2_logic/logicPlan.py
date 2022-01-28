# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'


class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()

    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()


def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    return logic.conjoin([A | B, (~A) % ((~B) | C), logic.disjoin([~A, ~B, C])])
    util.raiseNotDefined()


def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr('A')
    B = logic.Expr('B')
    C = logic.Expr('C')
    D = logic.Expr('D')

    return logic.conjoin([C % (B | D), A >> (~B & ~D), (~(B & ~C)) >> A, (~D) >> C])
    util.raiseNotDefined()


def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    WumpusAlive1 = logic.PropSymbolExpr('WumpusAlive', 1)
    WumpusAlive0 = logic.PropSymbolExpr('WumpusAlive', 0)
    WumpusBorn0 = logic.PropSymbolExpr('WumpusBorn', 0)
    WumpusKilled0 = logic.PropSymbolExpr('WumpusKilled', 0)

    State_0 = WumpusAlive1 % (
        (WumpusAlive0 & ~WumpusKilled0) | (~WumpusAlive0 & WumpusBorn0))
    State_1 = ~(WumpusAlive0 & WumpusBorn0)
    State_2 = WumpusBorn0

    return logic.conjoin(State_0, State_1, State_2)

    util.raiseNotDefined()


def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    sentence_CNF = logic.to_cnf(sentence)
    return logic.pycoSAT(sentence_CNF)
    util.raiseNotDefined()


def atLeastOne(literals):
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(literals)
    util.raiseNotDefined()


def atMostOne(literals):
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    con_literal = []
    for literal in literals:
        for another_literal in literals:
            if literal != another_literal:
                con_literal.append(~literal | ~another_literal)

    return logic.conjoin(con_literal)


def exactlyOne(literals):
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    con_literal = []
    for literal in literals:
        for another_literal in literals:
            if literal != another_literal:
                con_literal.append(~literal | ~another_literal)

    return logic.conjoin(con_literal) & logic.disjoin(literals)
    util.raiseNotDefined()


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    action_in_model = []
    for item in model.keys():
        item_parse = item.parseExpr(item)
        if item_parse[0] in actions and model[item]:
            action_in_model.append((item_parse[0], item_parse[1]))

    action_in_model = sorted(action_in_model, key=lambda x: int(x[1]))

    action_list = [temp[0] for temp in action_in_model]

    return action_list


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    discon = []
    wall_list = walls_grid.asList()

    if (x, y-1) not in wall_list:
        discon.append(logic.PropSymbolExpr(pacman_str, x, y-1, t-1)
                      & logic.PropSymbolExpr('North', t-1))
    if (x, y+1) not in wall_list:
        discon.append(logic.PropSymbolExpr(pacman_str, x, y+1, t-1)
                      & logic.PropSymbolExpr('South', t-1))
    if (x+1, y) not in wall_list:
        discon.append(logic.PropSymbolExpr(pacman_str, x+1, y, t-1)
                      & logic.PropSymbolExpr('West', t-1))
    if (x-1, y) not in wall_list:
        discon.append(logic.PropSymbolExpr(pacman_str, x-1, y, t-1)
                      & logic.PropSymbolExpr('East', t-1))

    return logic.PropSymbolExpr(pacman_str, x, y, t) % logic.disjoin(discon)


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """

    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    actions = ['North', 'South', 'East', 'West']
    con = []
    pacman_start_state = problem.getStartState()
    goal_state = problem.getGoalState()
    wall_list = walls.asList()

    # at time 0, there should be only one pacman:
    # if (x_i,y_i) has the pacman than ~(x_1,y_1)& ~(x_2,y_2)&..&(x_i,y_i)&...$(x_width,y_height)
    # (x,y) which is a wall is picked out.
    One_pacman_0 = [logic.PropSymbolExpr(
        pacman_str, pacman_start_state[0], pacman_start_state[1], 0)]
    for x in range(1, width+1):
        for y in range(1, height+1):
            if (x, y) not in wall_list and (x, y) != pacman_start_state:
                One_pacman_0.append(~logic.PropSymbolExpr(pacman_str, x, y, 0))
    con.append(logic.conjoin(One_pacman_0))

    t = 0
    while t < 50:
        # for each step,at time t, we should only choose exactly one direction to move:
        action_literals = [logic.PropSymbolExpr(act, t) for act in actions]
        action_ex_one = exactlyOne(action_literals)
        con.append(action_ex_one)

        # at t+1, we want pacman at the goal_state and goal_stae <==> (previous position at time t-1) & (took action to move to x, y)
        goal = logic.conjoin(logic.PropSymbolExpr(pacman_str, goal_state[0], goal_state[1], t+1),
                             pacmanSuccessorStateAxioms(goal_state[0], goal_state[1], t+1, walls))

        solution = findModel(logic.conjoin(con) & goal)

        if solution:
            return extractActionSequence(solution, actions)

        # If we get to here, we haven't found a solution yet.
        successor_list = []
        for x in range(1, width+1):
            for y in range(1, height+1):
                if (x, y) not in wall_list:
                    successor_list.append(
                        pacmanSuccessorStateAxioms(x, y, t+1, walls))
        successor = logic.conjoin(successor_list)
        con.append(successor)
        t = t+1

    return False


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    actions = ['North', 'South', 'East', 'West']
    con = []
    pacman_start_state = problem.getStartState()[0]
    food_list = problem.getStartState()[1].asList()
    wall_list = walls.asList()

    # at time 0, there should be only one pacman:
    # if (x_i,y_i) has the pacman than ~(x_1,y_1)& ~(x_2,y_2)&..&(x_i,y_i)&...$(x_width,y_height)
    # (x,y) which is a wall is picked out.
    One_pacman_0 = [logic.PropSymbolExpr(
        pacman_str, pacman_start_state[0], pacman_start_state[1], 0)]
    for x in range(1, width+1):
        for y in range(1, height+1):
            if (x, y) not in wall_list and (x, y) != pacman_start_state:
                One_pacman_0.append(~logic.PropSymbolExpr(pacman_str, x, y, 0))
    con.append(logic.conjoin(One_pacman_0))

    t = 0
    while t < 50:
        # for each step,at time t, we should only choose exactly one direction to move:
        action_literals = [logic.PropSymbolExpr(act, t) for act in actions]
        action_ex_one = exactlyOne(action_literals)
        con.append(action_ex_one)

        # at t+1, we want pacman at the goal_state and goal_stae <==> (previous position at time t-1) & (took action to move to x, y)
        # that is, at t+1 we should eat all of the food
        # we can eat any food at any time from 0 to t
        goal = []
        for food in food_list:
            eat_at_anytime = []
            for eat_time in range(0, t+1):
                eat_at_anytime.append(logic.PropSymbolExpr(
                    pacman_str, food[0], food[1], eat_time))
            goal.append(logic.disjoin(eat_at_anytime))
        solution = findModel(logic.conjoin(con) & logic.conjoin(goal))

        if solution:
            return extractActionSequence(solution, actions)

        # If we get to here, we haven't found a solution yet.
        successor_list = []
        for x in range(1, width+1):
            for y in range(1, height+1):
                if (x, y) not in wall_list:
                    successor_list.append(
                        pacmanSuccessorStateAxioms(x, y, t+1, walls))
        successor = logic.conjoin(successor_list)
        con.append(successor)
        t = t+1

    return False


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
