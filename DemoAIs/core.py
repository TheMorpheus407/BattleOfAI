import time

from DemoAIs.BOAIapi import BOAIapi


def turn(board, symbol):
    """
    TODO ITS YOUR TURN TO CODE THE AI!
    :param board: Contains the current state of the game
    :param symbol: Contains your symbol on the board - either X if you are the first player or O if you are the 2nd.
    :return: pos_x, pos_y where your AI wants to place a stone
    """

    for x in range(8):
        for y in range(8):
            if board[y][x] == "#":
                return x, y


#
# If you should find any bug in this API-Wrapper (or the API),
# please report it.
# Before this "ai" will at least do something, you have to change
# the login credentials in ".env" (see ".env.sample")
#
api = BOAIapi(turn, verbose=1)

while True:
    api.handle_available()
    time.sleep(5)
