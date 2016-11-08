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


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        "Create a search tree Node, derived from a parent by an action."
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def __lt__(self, node):
        return self.state < node.state

    def solution(self):
        "Return the sequence of actions to go from the root to this node."
        return [node.action for node in self.path()[1:]]

    def path(self):
        "Return a list of nodes forming the path from the root to this node."
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)



def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    stack = util.Stack()
    visited = []
    nodeStart = Node(problem.getStartState())

    if problem.isGoalState(nodeStart.state):
        return nodeStart.solution()

    stack.push(nodeStart)

    while stack:
        nodeParent = stack.pop()

        if problem.isGoalState(nodeParent.state):
            return nodeParent.solution()

        if nodeParent.state in visited:
            continue

        visited.append(nodeParent.state)

        for child in problem.getSuccessors(nodeParent.state):
            nodeChild = Node(child[0], nodeParent, child[1], child[2])
            stack.push(nodeChild)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    queue = util.Queue()
    visited = []
    nodeStart = Node(problem.getStartState())

    if problem.isGoalState(nodeStart.state):
        return nodeStart.solution()

    queue.push(nodeStart)

    while queue:
        nodeParent = queue.pop()

        if problem.isGoalState(nodeParent.state):
            return nodeParent.solution()

        if nodeParent.state in visited:
            continue

        visited.append(nodeParent.state)

        for child in problem.getSuccessors(nodeParent.state):
            nodeChild = Node(child[0], nodeParent, child[1], child[2])
            queue.push(nodeChild)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    pqueue = util.PriorityQueue()
    visited = []
    nodeStart = Node (problem.getStartState())

    if problem.isGoalState(nodeStart.state):
        return nodeStart.solution()

    pqueue.push(nodeStart, 0)

    while pqueue:
        nodeParent = pqueue.pop()

        if problem.isGoalState(nodeParent.state):
            return nodeParent.solution()

        if nodeParent.state in visited:
            continue

        visited.append(nodeParent.state)

        for child in problem.getSuccessors(nodeParent.state):
            nodeChild = Node(child[0], nodeParent, child[1], child[2])
            costG = problem.getCostOfActions(nodeChild.solution())
            pqueue.push(nodeChild, costG)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    pqueue = util.PriorityQueue()
    closed = []
    nodeStart = Node(problem.getStartState())

    if problem.isGoalState(nodeStart.state):
        return nodeStart.solution()

    pqueue.push(nodeStart, heuristic(nodeStart.state, problem))

    while pqueue:
        nodeParent = pqueue.pop()

        if problem.isGoalState(nodeParent.state):
            return nodeParent.solution()

        if nodeParent.state in closed:
            continue

        closed.append(nodeParent.state)

        for child in problem.getSuccessors(nodeParent.state):
            nodeChild = Node(child[0], nodeParent, child[1], child[2])
            costG = problem.getCostOfActions(nodeChild.solution())
            costF = costG + heuristic(nodeChild.state, problem)
            pqueue.push(nodeChild, costF)




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
