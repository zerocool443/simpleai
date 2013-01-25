#!/usr/bin/env python
# coding: utf-8

import math
from simpleai.search import SearchProblem, astar

MAP = """
##############################
#         #              #   #
# ####    ########       #   #
#  o #    #              #   #
#    ###     ####   ######   #
#         ####      #        #
#            #  #   #   #### #
#     ######    #       # x  #
#        #      #            #
##############################
"""
MAP = [list(x) for x in MAP.split("\n") if x]

COSTS = {
    "up": 10,
    "down": 10,
    "left": 10,
    "right": 10,
    "up left": 14,
    "up right": 14,
    "down left": 14,
    "down right": 14,
}


class GameWalkPuzzle(SearchProblem):

    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)
        for y in xrange(len(self.board)):
            for x in xrange(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        super(GameWalkPuzzle, self).__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state

        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1

        new_state = (x, y)
        return new_state

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)


def main():
    problem = GameWalkPuzzle(MAP)
    result = astar(problem, graph_search=True)
    path = [x[1] for x in result.path()]

    for y in xrange(len(MAP)):
        for x in xrange(len(MAP[y])):
            if (x, y) == problem.initial:
                print "o",
            elif (x, y) == problem.goal:
                print "x",
            elif (x, y) in path:
                print "·",
            else:
                print MAP[y][x],
        print


if __name__ == "__main__":
    main()
