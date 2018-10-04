#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md

import abalone
from GameMicroservice.DomainModel.GameInstance import GameInstance


class AbaloneInstance(GameInstance):
    GAME_NAME = "Abalone"
    AMOUNT_PLAYERS = 2

    def initialize_board(self):
        self.game = abalone.Game()
        self.update_player()
        return self.game.board

    def turn(self, vars):
        self.update_player()
        self.game.move(vars[0], vars[1])
        self.board = self.game.board

    def valid(self, vars):
        if len(vars) != 2:
            return False

        marbles = vars[0]
        direction = vars[1]

        if type(marbles) != list or type(direction) != int:
            return False

        if direction < 0 or direction > 6:
            return False

        try:
            self.update_player()
            for marble in marbles:
                if game.is_opponent(marble) or abalone.neighbor(marble, direction) == 0:
                    return False

            test_game = self.game.copy()
            test_game.move(marbles, direction)
        except:
            return False

        return True

    def won_check(self):
        return self.game.score['p1'] == 0 or self.game.score['p2'] == 0

    def update_player(self):
        # self.game.current_player in [1, 2]
        # self.activate_player in [0, 1]
        if self.game.current_player - 1 != self.active_player:
            self.game.toggle_player()
