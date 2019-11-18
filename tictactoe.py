# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 22:29:26 2019

@author: Vit Saidl
"""

import copy
from typing import List


class Game:
    """Represents tic-tac-toe game including input from human player and
    mnimax algorithm for choosing computer moves
    """

    MAX_DEPTH = 50

    def __init__(self) -> None:
        """Game initialization

        First two parameters of GameBoard should not be greater than 3.
        Although the program uses minimax with alpha-beta pruning, game boards
        larger than default one result in the freeze of game.
        """
        self.turn = 0
        self.new_board = GameBoard(3, 3, 3)
        self.realise_game_loop()

    def get_human_input(self) -> None:
        """Returns x and y coordinates of player's move.

        Returns:
            (int, int): x and y coordinates (0 to the length of axis)
        """
        max_x_included = self.new_board.no_rows
        max_y_included = self.new_board.no_columns
        choice_x = int(input(f"Insert x coordinate (1 to {max_x_included}): "))
        choice_y = int(input(f"Insert y coordinate (1 to {max_y_included}): "))
        return choice_x - 1, choice_y - 1

    def eval_play(
        self, board: "GameBoard", player: str, depth: int, alpha: int, beta
    ) -> int:
        """Evaluating possible players's (both human and ai) moves given
        certain game board state

        Used algorithm - minimax with alpha-beta pruning

        Args:
            board(GameBoard): Hyphotetical game board
            player(str): Player's symbol - either "X" or "O"
            depth(int): Level of game board tree state
            alpha(int): Best value representing game state that maximizer can
            guarantee on this level and levels above it
            beta(int): Best value representing game state that minimizer can
            guarantee on this level and levels above it

        Returns:
            int: Number evaluating given game board state; positive number = \
            X wins, negative number = O wins, zero = no one wins
        """

        who_is_winner = board.get_winner()
        if who_is_winner != 0:
            return who_is_winner
        elif board.is_every_field_filled():
            return 0
        elif depth > Game.MAX_DEPTH:
            return 0

        next_player = "X" if player == "O" else "O"

        if player == "X":
            max_eval = -999999
            for row_index, column_index, element in board:  # maximize_play
                if element == " ":
                    next_board = copy.deepcopy(board)
                    next_board.game_board[row_index][column_index] = player
                    eval_param = self.eval_play(
                        next_board, next_player, depth + 1, alpha, beta
                    )
                    max_eval = max(max_eval, eval_param)
                    alpha = max(alpha, eval_param)
                    if beta <= alpha:
                        break
            return max_eval

        else:
            min_eval = 999999
            for row_index, column_index, element in board:  # minimize_play
                if element == " ":
                    next_board = copy.deepcopy(board)
                    next_board.game_board[row_index][column_index] = player
                    eval_param = self.eval_play(
                        next_board, next_player, depth + 1, alpha, beta
                    )
                    min_eval = min(min_eval, eval_param)
                    beta = min(beta, eval_param)
                    if beta <= alpha:
                        break
            return min_eval

    def ai_plays(self, player: str, game_board: "GameBoard") -> None:
        """Realise the ai play immediate following player's play

        AI looks at its possible plays and choose the best one for itself.

        Args:
            player(str): ai player symbol ("O" or "X", usually "O")
            game_board(GameBoard): real game board (not hypothetical board from
            tree traversal through potential board states)
        """
        possible_states = []
        next_player = "X" if player == "O" else "O"
        actual_tree_depth = 0
        for row_index, column_index, element in game_board:
            if element == " ":
                next_board = copy.deepcopy(game_board)
                next_board.game_board[row_index][column_index] = player
                possible_states.append(
                    (
                        next_board,
                        self.eval_play(
                            next_board,
                            next_player,
                            actual_tree_depth + 1,
                            -999999,
                            999999,
                        ),
                    )
                )
        best_play = min(
            possible_states, key=lambda board_and_score: board_and_score[1]
        )[0]
        self.new_board = best_play

    def realise_game_loop(self) -> None:
        """Realises game loop

        Alternates between computer and human moves, gets input from human,
        traverses minimax tree for computer and shows who the winner is.
        """
        game_continues = True
        while game_continues:
            self.turn += 1
            human_player_turn = self.turn % 2 == 1
            if human_player_turn:
                necessary_human_input = True
                while necessary_human_input:
                    print("Player X:")
                    choice_x, choice_y = self.get_human_input()
                    necessary_human_input = not self.new_board.insert_symbol(
                        choice_x, choice_y, "X",
                    )
            else:
                print("Player O plays")
                self.ai_plays("O", self.new_board)

            game_continues = False
            self.new_board.print_pretty_board()
            winner = self.new_board.get_winner()
            if winner > 0:
                print("X wins")
            elif winner < 0:
                print("O wins")
            elif self.new_board.is_every_field_filled():
                print("No one wins")
            else:
                game_continues = True


class GameBoard:
    """Represents game board on which the tic-tac-toe game takes place
    """

    PLAYER_X_WON = 100
    PLAYER_O_WON = -100
    NO_ONE_WON = 0

    def __init__(
        self, no_columns: int, no_rows: int, number_to_win: int
    ) -> None:
        """Initialization of new game board

        Args:
            no_columns(int): Number of columns
            no_rows(int): Number of rows
            number_to_win(int): Length of character line necessary for winning
        """
        self.no_columns = no_columns
        self.no_rows = no_rows
        self.game_board = [[" "] * no_columns for _ in range(no_rows)]
        self.number_to_win = number_to_win

    def insert_symbol(self, row: int, column: int, symbol: str) -> bool:
        """Inserts player symbol into the game board

        Args:
            row(int): Row index
            column(int): Column index
            symbol(string): Player symbol (either X or O)

        Returns:
            bool: True if symbol is inserted, False if coordinates were not valid
        """
        if row >= self.no_rows or column >= self.no_columns:
            print("Index larger than board axis")
            return False
        elif self.game_board[row][column] != " ":
            print("Field already used")
            return False
        self.game_board[row][column] = symbol
        return True

    def is_every_field_filled(self) -> None:
        """Examine if every filed in game board is filled

        Returns:
            bool: True if all elements are filled, otherwise False
        """
        for row in self.game_board:
            for element in row:
                if element == " ":
                    return False
        return True

    def _examine_row(self, row: List[str]) -> int:
        """Looks for self.number_to_win long uninterrupted line of the same
        player symbols

        Args:
            row (List[str]): One line of game board

        Returns:
            int: One of constants regarding the winner identity
        """
        number_of_x = 0
        number_of_o = 0
        for element in row:
            if element == "X":
                number_of_x += 1
                number_of_o = 0
            elif element == "O":
                number_of_x = 0
                number_of_o += 1
            else:
                number_of_x = 0
                number_of_o = 0
            if number_of_x == self.number_to_win:
                return GameBoard.PLAYER_X_WON
            elif number_of_o == self.number_to_win:
                return GameBoard.PLAYER_O_WON
        return GameBoard.NO_ONE_WON

    def _examine_rows(self) -> int:
        """Looks through all rows in order to find self.number_to_win long
        uninterrupted line of the same player symbols

        Returns:
            int: If returned number > 0, player "X" has won. Number < 0 means \
            that player "O" has won. Number equal zero means no one has won \
            (either all fields are occupied or game still continues)
        """
        result_rows = GameBoard.NO_ONE_WON
        for row in self.game_board:
            result_rows += self._examine_row(row)
        return result_rows

    def _examine_column(self, column_index):
        """Looks for self.number_to_win long uninterrupted line of the same
        player symbols

        Args:
            column_index (int): Index of column for examination

        Returns:
            int: One of constants specifying the winner identity
        """
        number_of_x = 0
        number_of_o = 0
        for row in self.game_board:
            if row[column_index] == "X":
                number_of_x += 1
                number_of_o = 0
            elif row[column_index] == "O":
                number_of_x = 0
                number_of_o += 1
            else:
                number_of_x = 0
                number_of_o = 0

            if number_of_x == self.number_to_win:
                return GameBoard.PLAYER_X_WON

            elif number_of_o == self.number_to_win:
                return GameBoard.PLAYER_O_WON
        return GameBoard.NO_ONE_WON

    def _examine_columns(self):
        """Looks through all columns in order to find self.number_to_win long
        uninterrupted line of the same player symbols

        Returns:
            int: If returned number > 0, player "X" has won. Number < 0 means \
            that player "O" has won. Number equal zero means no one has won \
            (either all fields are occupied or game still continues)
        """
        result_columns = GameBoard.NO_ONE_WON
        for column_index in range(self.no_columns):
            result_columns += self._examine_column(column_index)
        return result_columns

    def _left_to_right_upper_diag(self, max_start_column: int) -> int:
        """Looks for self.number_to_win long uninterrupted line of the same
        player symbols in diagonal

        Examined are positions from main diagonal left-right (i. e. going from
        upper left corner to lower right corner) towards mini-diagonals above
        that (main diagonal is included).

        Args:
            max_start_column (int): Columns with this and higher indices are
            not relevant - diagonal is shorter than self.number_to_win

        Returns:
            int: One of constants specifying the winner identity
        """
        for i in range(0, max_start_column):
            number_of_x = 0
            number_of_o = 0
            j = 0
            while i < self.no_columns and j < self.no_rows:
                if self.game_board[j][i] == "X":
                    number_of_x += 1
                    number_of_o = 0
                elif self.game_board[j][i] == "O":
                    number_of_x = 0
                    number_of_o += 1
                else:
                    number_of_x = 0
                    number_of_o = 0
                if number_of_x == self.number_to_win:
                    return GameBoard.PLAYER_X_WON
                elif number_of_o == self.number_to_win:
                    return GameBoard.PLAYER_O_WON
                i += 1
                j += 1
        return GameBoard.NO_ONE_WON

    def _left_to_right_lower_diag(self, max_start_row: int) -> int:
        """Looks for self.number_to_win long uninterrupted line of the same
        player symbols in diagonal

        Examined are positions from main diagonal left-right (i. e. going from
        upper left corner to lower right corner) towards mini-diagonals below
        that (main diagonal is not included).

        Args:
            max_start_row (int): Rows with this and higher indices are
            not relevant - diagonal is shorter than self.number_to_win

        Returns:
            int: One of constants specifying the winner identity
        """
        for j in range(1, max_start_row):
            number_of_x = 0
            number_of_o = 0
            i = 0
            while i < self.no_columns and j < self.no_rows:
                if self.game_board[j][i] == "X":
                    number_of_x += 1
                    number_of_o = 0
                elif self.game_board[j][i] == "O":
                    number_of_x = 0
                    number_of_o += 1
                else:
                    number_of_x = 0
                    number_of_o = 0
                if number_of_x == self.number_to_win:
                    return GameBoard.PLAYER_X_WON
                elif number_of_o == self.number_to_win:
                    return GameBoard.PLAYER_O_WON
                i += 1
                j += 1
        return GameBoard.NO_ONE_WON

    def _right_to_left_upper_diag(self, max_start_column):
        """Looks for self.number_to_win long uninterrupted line of the same
        player symbols in diagonal

        Examined are positions from main diagonal right-left (i. e. going from
        lower left corner to upper right corner) towards mini-diagonals above
        that (main diagonal is included).

        Args:
            max_start_column (int): Columns with this and higher indices are
            not relevant - diagonal is shorter than self.number_to_win

        Returns:
            int: One of constants specifying the winner identity
        """
        for i in range(self.no_columns - 1, max_start_column - 1, -1):
            number_of_x = 0
            number_of_o = 0
            j = 0
            while i >= 0 and j < self.no_rows:
                if self.game_board[j][i] == "X":
                    number_of_x += 1
                    number_of_o = 0
                elif self.game_board[j][i] == "O":
                    number_of_x = 0
                    number_of_o += 1
                else:
                    number_of_x = 0
                    number_of_o = 0
                if number_of_x == self.number_to_win:
                    return GameBoard.PLAYER_X_WON
                elif number_of_o == self.number_to_win:
                    return GameBoard.PLAYER_O_WON
                i -= 1
                j += 1
        return GameBoard.NO_ONE_WON

    def _right_to_left_lower_diag(self, max_start_row: int) -> int:
        """Looks for self.number_to_win long uninterrupted line of the same
        player symbols in diagonal

        Examined are positions from main diagonal right-left (i. e. going from
        lower left corner to upper right corner) towards mini-diagonals below
        that (main diagonal is not included).

        Args:
            max_start_row (int): Rows with this and higher indices are
            not relevant - diagonal is shorter than self.number_to_win

        Returns:
            int: One of constants specifying the winner identity
        """
        for j in range(1, max_start_row):
            number_of_x = 0
            number_of_o = 0
            i = self.no_columns - 1
            while i >= 0 and j < self.no_rows:
                if self.game_board[j][i] == "X":
                    number_of_x += 1
                    number_of_o = 0
                elif self.game_board[j][i] == "O":
                    number_of_x = 0
                    number_of_o += 1
                else:
                    number_of_x = 0
                    number_of_o = 0
                if number_of_x == self.number_to_win:
                    return GameBoard.PLAYER_X_WON
                elif number_of_o == self.number_to_win:
                    return GameBoard.PLAYER_O_WON
                i -= 1
                j += 1
        return GameBoard.NO_ONE_WON

    def _examine_diagonals(self) -> int:
        """Looks through all diagonals in order to find self.number_to_win long
        uninterrupted line of the same player symbols

        Returns:
            int: If returned number > 0, player "X" has won. Number < 0 means \
            that player "O" has won. Number equal zero means no one has won \
            (either all fields are occupied or game still continues)
        """
        result_diagonal = GameBoard.NO_ONE_WON
        max_start_column = self.no_columns - self.number_to_win + 1
        max_start_row = self.no_rows - self.number_to_win + 1
        result_diagonal += self._left_to_right_upper_diag(max_start_column)
        result_diagonal += self._left_to_right_lower_diag(max_start_row)
        result_diagonal += self._right_to_left_upper_diag(max_start_column)
        result_diagonal += self._right_to_left_lower_diag(max_start_row)
        return result_diagonal

    def get_winner(self) -> None:
        """Looks through all rows, columns abd diagonals in order to find
        self.number_to_win long uninterrupted line of the same player symbols

        Returns:
            int: If returned number > 0, player "X" has won. Number < 0 means \
            that player "O" has won. Number equal zero means no one has won \
            (either all fields are occupied or game still continues)
        """
        result_global = GameBoard.NO_ONE_WON
        result_global += self._examine_rows()
        result_global += self._examine_columns()
        result_global += self._examine_diagonals()
        return result_global

    def print_pretty_board(self) -> None:
        """Prints game board to console output
        """
        print("_" * (2 * self.no_columns + 1))
        for row in self.game_board:
            printed_row = "|"
            for column_elem in row:
                printed_row += column_elem + "|"
            print(printed_row)
        print("\u00AF" * (2 * self.no_columns + 1))

    def __iter__(self) -> None:
        """Enables iteration through game board fields
        """
        for row_index in range(self.no_rows):
            for column_index in range(self.no_columns):
                yield row_index, column_index, self.game_board[row_index][
                    column_index
                ]


game = Game()
