# -*- coding: utf-8 -*-

# Documentation available at https://scriptim.github.io/Abalone-BoAI/

import time
from random import choice

# Make sure "abalone-boai" (https://pypi.org/project/abalone-boai/) is installed
from abalone.abstract_player import AbstractPlayer

from DemoAIs.BOAIapi import BOAIapi


class DemoPlayer(AbstractPlayer):

    def turn(self, game, moves_history):
        """
        TODO ITS YOUR TURN TO CODE THE AI!
        See https://scriptim.github.io/Abalone-BoAI/abstract_player.html#abalone.abstract_player.AbstractPlayer.turn\
        for details.
        :param game: The current state of the Game
        :param moves_history: A chronologically sorted list of all past moves, starting with the earliest. It also\
            contains the opponent's moves. The elements correspond to the return values of the AbstractPlayer.turn()\
            method. THIS IS CURRENTLY UNSUPPORTED AND WILL ALWAYS BE `None`!
        """

        # return a random legal move
        return choice(list(game.generate_legal_moves()))


#
# If you should find any bug in this API-Wrapper (or the API),
# please report it.
# Before this "ai" will at least do something, you have to change
# the login credentials in ".env" (see ".env.sample")
#
demo_player = DemoPlayer()
api = BOAIapi(demo_player.turn, verbose=1)

while True:
    api.handle_available()
    time.sleep(5)
