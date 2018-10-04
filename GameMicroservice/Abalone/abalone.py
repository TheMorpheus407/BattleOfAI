#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md

rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
diagonals = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

spaces = [
    'A1', 'A2', 'A3', 'A4', 'A5',
    'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
    'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8',
    'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
    'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
    'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
    'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
    'I5', 'I6', 'I7', 'I8', 'I9'
]


class Game:
    """Representation of an Abalone game.
    """

    def __init__(self):
        """Initialize the game.
        """

        # black (X) = 1, white (O) = 2
        # Note that the AI is passed a modified board with its own marbles
        # represented by 1 and the opponent's marbles by -1.
        self.current_player = 1

        # Maps a space of the board to the player (1/2) to own it or 0 if the
        # space is empty. See the documentation for information on how the
        # spaces are denoted.
        self.board = {}

        self.fill_board()
        # The score of a player decrements whenever a marble is pushed off the
        # board by the opponent.
        self.score = {'p1': 6, 'p2': 6}

    def broadside(self, marbles, direction):
        """Perform a broadside move.

        .. warning:: This function should not be called directly, as it does
                     not perform input validation, which could lead to
                     unpredictable behavior. It is only intended as a help
                     function for :func:`move`.

        :param marbles: the marbles to be moved
        :type marbles: list[str]
        :param direction: the direction of movement

        .. seealso:: :func:`move` for information on the direction parameter

        :type direction: int
        """

        for marble in marbles:
            self.move([marble], direction)

    def copy(self):
        """Make a clone of the current state of the game.

        :return: the clone
        :rtype: Game
        """

        game_copy = Game()
        game_copy.current_player = self.current_player
        game_copy.board = self.board.copy()
        game_copy.score = self.score.copy()

        return game_copy

    def fill_board(self):
        """Fill the ``board`` dict with the `default initial position
        <https://en.wikipedia.org/wiki/File:Abalone_standard.svg>`_.
        """

        global rows
        global diagonals

        for row in rows:
            row_index = rows.index(row)

            diagonals_for_row = (diagonals[0:5 + row_index] if
                                 row_index <= 4 else diagonals[row_index - 4:])

            for diagonal in diagonals_for_row:
                self.board[row + diagonal] = 0  # empty
                if (row in ['A', 'B'] or
                        (row == 'C' and diagonal in ['3', '4', '5'])):
                    self.board[row + diagonal] = 1  # black
                elif (row in ['H', 'I'] or
                      (row == 'G' and diagonal in ['5', '6', '7'])):
                    self.board[row + diagonal] = 2  # white

    def in_line(self, marbles, direction):
        """Perform an in-line move, sumito if applicable.

        .. warning:: This function should not be called directly, as it does
                     not perform input validation, which could lead to
                     unpredictable behavior. It is only intended as a help
                     function for :func:`move`.

        :param marbles: the marbles to be moved
        :type marbles: list[str]
        :param direction: the direction of movement

        .. seealso:: :func:`move` for information on the direction parameter

        :type direction: int
        :raises IllegalMoveException: *space* is not empty

        if the destination space is already occupied

        :raises IllegalMoveException: Moving *n* marbles with *m* own marble(s)

        if the move cannot be made due to too few marbles
        """

        head = from_head_to_tail(marbles, direction)[0]

        # destination: opponent -> sumito
        opponent_marbles = []
        if self.is_opponent(neighbor(head, direction)):
            opponent_head = neighbor(head, direction)
            opponent_marbles = [opponent_head]
            while True:
                next_marble = neighbor(opponent_head, direction)
                if self.is_opponent(next_marble):
                    opponent_head = next_marble
                    opponent_marbles.append(next_marble)
                elif self.is_current_player(next_marble):
                    # The space after the opponent's line of marbles is already
                    # owned by the player, hence not empty.
                    raise IllegalMoveException(f'{next_marble} is not empty')
                else:
                    break

            # Valid sumito moves are 2 -> 1, 3 -> 1, 3 -> 2
            if len(opponent_marbles) >= len(marbles):
                raise IllegalMoveException(f'Moving {len(opponent_marbles)} '
                                           f'marbles with {len(marbles)} '
                                           'own marble(s)')

        # The list starts with the marble closest to the current player's
        # marbles which must be moved last.
        opponent_marbles.reverse()
        for opponent_marble in opponent_marbles:
            self.move([opponent_marble], direction)

        # destination: current player
        if self.is_current_player(neighbor(head, direction)):
            raise IllegalMoveException(f'{neighbor(head, direction)} is not '
                                       'empty')

        # destination: empty
        for marble in from_head_to_tail(marbles, direction):
            self.move([marble], direction)

    def is_current_player(self, space):
        """Check if a space is owned by the current player.

        :param space: the space to be checked
        :type space: str
        :return: whether the space is owned by the current player
        :rtype: bool
        """

        if space == 0:
            return False
        return self.board[parse_space(space)] == self.current_player

    def is_empty(self, space):
        """Check if a space is empty.

        :param space: the space to be checked
        :type space: str
        :return: whether the space is empty
        :rtype: bool
        """

        if space == 0:
            return False
        empty = self.board[parse_space(space)] == 0
        return empty

    def is_opponent(self, space):
        """Check if a space is owned by the opponent player.

        :param space: the space to be checked
        :type space: str
        :return: whether the space is owned by the opponent player
        :rtype: bool
        """

        if space == 0:
            return False
        return (self.board[parse_space(space)] == 2 if
                self.current_player == 1 else
                self.board[parse_space(space)] == 1)

    def move(self, marbles, direction):
        """Perform a move in a specific direction.

        :param marbles: the marbles to be moved
        :type marbles: list[str]
        :param direction: the direction of movement

        ::

            6 1
            5 · 2
            4 3

        1. northeast
        2. east
        3. southeast
        4. southwest
        5. west
        6. northwest

        :type direction: int
        :raises IllegalMoveException: Moving *n* marbles

        if the number of marbles is not between ``1`` and ``3`` (inclusive)

        :raises IllegalMoveException: Marbles are not in a straight line
        :raises IllegalMoveException: *space* is not empty
        """

        marbles = [parse_space(marble) for marble in marbles]

        if len(marbles) < 1 or len(marbles) > 3:
            raise IllegalMoveException(f'Moving {len(marbles)} marbles')
        if not are_straight_line(marbles):
            raise IllegalMoveException(
                f'Marbles {", ".join(marbles)} are not in a straight line')

        # single
        if len(marbles) == 1:
            destination = neighbor(marbles[0], direction)
            if destination == 0:
                self.on_off_board(self.board[marbles[0]])
            elif not self.is_empty(destination):
                raise IllegalMoveException(f'{destination} is not empty')
            else:
                self.board[destination] = self.board[marbles[0]]
            self.board[marbles[0]] = 0
            return

        same = same_row_and_diagonal(marbles)
        if (same['row'] and direction in [1, 3, 4, 6] or
            same['diagonal'] and direction in [1, 2, 4, 5] or
                same['diagonal_r'] and direction in [2, 3, 5, 6]):
            self.broadside(marbles, direction)
        else:
            self.in_line(marbles, direction)

    def on_off_board(self, player):
        """Reduce the score of a player whose marble has been pushed off the
        board.

        :param player: the player (``1`` or ``2``)
        :type player: int
        """

        index = f'p{player}'
        self.score[index] = self.score[index] - 1

    def print_board(self):
        """Print the board to stdout.

        Player 1 (black) is represented by ``X``, player 2 (white) by ``O``,
        empty spaces by ``·``, e. g.

        ::

              I O O O O O
             H O O O O O O
            G · · O O O · ·
           F · · · · · · · ·
          E · · · · · · · · ·
           D · · · · · · · · 9
            C · · X X X · · 8
             B X X X X X X 7
              A X X X X X 6
                 1 2 3 4 5
        """

        # black = X, white = O, empty = ·
        log_board = {}
        for space in self.board:
            log_board[space] = ('X' if self.board[space] == 1 else
                                ('O' if self.board[space] == 2 else '·'))

        rows = {}
        rows['A'] = " ".join([str(log_board[f"A{d}"]) for d in range(1, 6)])
        rows['B'] = " ".join([str(log_board[f"B{d}"]) for d in range(1, 7)])
        rows['C'] = " ".join([str(log_board[f"C{d}"]) for d in range(1, 8)])
        rows['D'] = " ".join([str(log_board[f"D{d}"]) for d in range(1, 9)])
        rows['E'] = " ".join([str(log_board[f"E{d}"]) for d in range(1, 10)])
        rows['F'] = " ".join([str(log_board[f"F{d}"]) for d in range(2, 10)])
        rows['G'] = " ".join([str(log_board[f"G{d}"]) for d in range(3, 10)])
        rows['H'] = " ".join([str(log_board[f"H{d}"]) for d in range(4, 10)])
        rows['I'] = " ".join([str(log_board[f"I{d}"]) for d in range(5, 10)])

        board_str = (f'    I {rows["I"]}\n'
                     f'   H {rows["H"]}\n'
                     f'  G {rows["G"]}\n'
                     f' F {rows["F"]}\n'
                     f'E {rows["E"]}\n'
                     f' D {rows["D"]} 9\n'
                     f'  C {rows["C"]} 8\n'
                     f'   B {rows["B"]} 7\n'
                     f'    A {rows["A"]} 6\n'
                     f'       1 2 3 4 5')

        print(board_str)

    def toggle_player(self):
        """Switch ``current_player`` between ``1`` and ``2``.
        """

        self.current_player = 2 if self.current_player == 1 else 1


class IllegalMoveException(Exception):
    """Custom Exception to be raised whenever a player performs an illegal
    move.
    """

    pass


def are_straight_line(spaces):
    """Check if the given spaces form a straight line.

    This is a required for a valid move.

    :param spaces: a list of spaces
    :type spaces: list[str]
    :return: whether the spaces form a straight line
    :rtype: bool
    """

    spaces = [parse_space(space) for space in spaces]

    if len(spaces) <= 1:
        return True

    # Check for duplicates.
    if len(set(spaces)) != len(spaces):
        return False

    same = same_row_and_diagonal(spaces)
    if not same['row'] and not same['diagonal'] and not same['diagonal_r']:
        return False

    # The lexicographical sorting ensures that successive spaces in the list
    # are closest to each other on the board.
    spaces.sort()
    for space in range(1, len(spaces)):
        prev_row = spaces[space - 1][0]
        row = spaces[space][0]
        delta_row = abs(rows.index(prev_row) - rows.index(row))

        prev_diagonal = spaces[space - 1][1]
        diagonal = spaces[space][1]
        delta_diagonal = (abs(diagonals.index(prev_diagonal) -
                              diagonals.index(diagonal)))

        # The distance (delta) to the previous space is exactly 1 if they are
        # adjacent.
        if (same['row'] and delta_diagonal != 1 or
            same['diagonal'] and delta_row != 1 or
                same['diagonal_r'] and (delta_diagonal != 1 or
                                        delta_row != 1)):
            return False

    return True


def from_head_to_tail(spaces, direction):
    """Sort a straight line of spaces by a certain direction so that the head
    comes first.

    :param spaces: a straight line of spaces
    :type spaces: list[str]
    :param direction: the direction in which the spaces are oriented

    .. seealso:: :func:`move` for information on the direction parameter

    :type direction: int
    :raises Exception: Marbles are not in a straight line
    :raises Exception: Moving *marbles* in direction is not an in-line move
    :return: a sorted list of spaces
    :rtype: list[str]
    """

    if not are_straight_line(spaces):
        raise Exception(f'Marbles {", ".join(spaces)} '
                        'are not in a straight line')
    same = same_row_and_diagonal(spaces)
    if (same['row'] and direction in [1, 3, 4, 6] or
        same['diagonal'] and direction in [1, 2, 4, 5] or
            same['diagonal_r'] and direction in [2, 3, 5, 6]):
        raise Exception(f'Moving {", ".join(spaces)} in direction {direction} '
                        'is not an in-line move')
    spaces.sort()
    if direction in [1, 2, 6]:
        spaces.reverse()
    return spaces


def neighbor(space, direction):
    """Get the adjacent space in a certain direction.

    :param space: the space from which the neighbour is determined
    :type space: str
    :param direction: the direction

    .. seealso:: :func:`move` for information on the direction parameter

    :type direction: int
    :raises Exception: Invalid direction

    if the direction is not between ``1`` and ``6`` (inclusive)

    :return: the neighbor space in standard notation | ``0`` if there is no
            neighbor in the given direction

    :rtype: str | int
    """

    space = parse_space(space)

    row = rows.index(space[0])
    diagonal = diagonals.index(space[1])

    if direction == 1:
        row = row + 1
        diagonal = diagonal + 1
    elif direction == 2:
        diagonal = diagonal + 1
    elif direction == 3:
        row = row - 1
    elif direction == 4:
        row = row - 1
        diagonal = diagonal - 1
    elif direction == 5:
        diagonal = diagonal - 1
    elif direction == 6:
        row = row + 1
    else:
        raise Exception(f'Invalid direction {direction}')

    if (row < 0 or row >= len(rows) or
        diagonal < 0 or diagonal >= len(diagonals) or
            not f'{rows[row]}{diagonals[diagonal]}' in spaces):
        return 0  # off the board

    return rows[row] + diagonals[diagonal]


def parse_space(space):
    """Convert any valid space notation to the standard notation.

    A valid string that denotes a space consists of a row letter (from ``A`` to
    ``I``) and a diagonal number (from ``1`` to ``9``). The notation is
    case-insensitive and does not require a specific order.

    The standard notation starts with a capital row letter followed by a
    diagonal number. It is used for the keys in the ``board`` dict, among
    other things.

    :param space: a space in any valid notation
    :type space: str
    :raises TypeError: Invalid type (str expected)
    :raises Error: Invalid string length (2 expected)
    :raises Error: Invalid string notation
    :return: the standard notation for the given space
    :rtype: str
    """

    if (space == 0):
        return 0  # off the board

    if not isinstance(space, str):
        raise TypeError(f'Invalid type \'{type(space).__name__}\' '
                        '(str expected)')
    if len(space) != 2:
        raise Error(f'Invalid string length {len(space)} (2 expected)')

    space = space.upper()

    if space[0] in rows and space[1] in diagonals:
        return space
    elif space[0] in diagonals and space[1] in rows:
        return space[::-1]

    raise Error(f'Invalid string notation {space}')


def same_row_and_diagonal(spaces):
    """Indicate if the given spaces are in the same row and/or diagonal.

    :param spaces: a list of spaces
    :type spaces: list[str]
    :return: a dict with three keys ``row``, ``diagonal`` and ``diagonal_r``

    - ``row`` is ``True`` if the spaces are in the same row (``A`` to ``I``).
    - ``diagonal`` is ``True`` if the spaces are in the same diagonal (``1`` to
      ``9``). This includes only the diagonals from northwest to southeast.
    - ``diagonal_r`` is ``True`` if the spaces are in the same diagonal. This
      includes only the diagonals from northeast to southwest.

    :rtype: dict[str, bool]
    """

    global rows
    global diagonals

    spaces = [parse_space(space) for space in spaces]
    same_row = True
    same_diagonal = True
    same_diagonal_r = True
    for space in range(1, len(spaces)):
        delta_row = (abs(rows.index(spaces[0][0]) -
                         rows.index(spaces[space][0])))
        delta_diagonal = (abs(diagonals.index(spaces[0][1]) -
                              diagonals.index(spaces[space][1])))

        if delta_row != 0:
            same_row = False

        if delta_diagonal != 0:
            same_diagonal = False

        if delta_row != delta_diagonal:
            same_diagonal_r = False

    return {
        'row': same_row,
        'diagonal': same_diagonal,
        'diagonal_r': same_diagonal_r
    }
