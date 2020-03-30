# -*- coding: utf-8 -*-

import sys
from copy import deepcopy

from GameMicroservice.DomainModel.GameInstance import GameInstance

sys.path.insert(0, '/app/GameMicroservice/Abalone/Abalone-BoAI/abalone')

from enums import Direction, Marble, Space
from game import Game, IllegalMoveException


def _vars_to_move_args(vars):
    if 'marble2' not in vars or vars['marble2'] == '':
        marbles = Space[vars['marble1']]
    else:
        marbles = (Space[vars['marble1']], Space[vars['marble2']])
    direction = Direction[vars['direction']]

    return marbles, direction


def _serializable_board(board):
    board = deepcopy(board)
    for row in range(len(board)):
        for space in range(len(board[row])):
            board[row][space] = board[row][space].name

    return board


class AbaloneInstance(GameInstance):
    GAME_NAME = "Abalone"
    AMOUNT_PLAYERS = 2

    def __init__(self, id, active_player=0, history=None, *args, **kwargs):
        self.state = Game()

        # update state because a new instance is created before every turn and previous state cannot be accessed
        if history is not None:
            board = deepcopy(history[-1])
            for row in range(len(board)):
                for col in range(len(board[row])):
                    board[row][col] = Marble[board[row][col]]
            self.state.board = board
            if active_player == 1:
                self.state.switch_player()

        super().__init__(id, active_player, history, *args, **kwargs)

    def initialize_board(self):
        return _serializable_board(self.state.board)

    def turn(self, vars):
        self.state.move(*_vars_to_move_args(vars))
        self.board = _serializable_board(self.state.board)

    def valid(self, vars):
        game = deepcopy(self.state)
        try:
            game.move(*_vars_to_move_args(vars))
            return True
        except IllegalMoveException as ex:
            return False

    def won_check(self):
        score = self.state.get_score()
        if 8 not in score:
            return False

        self.won(0 if score[0] == 8 else 1)

        return True

    def next_player(self):
        self.state.switch_player()
        super().next_player()
