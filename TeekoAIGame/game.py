import math
import random
import copy


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    weight = [
                [1, 3, 1, 3, 1],
                [2, 3, 3, 3, 2],
                [2, 3, 4, 3, 2],
                [2, 3, 3, 3, 2],
                [1, 2, 2, 2, 1]
             ]

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        count = 0  # TODO: detect drop phase
        for i in range(5):
            for j in range(5):
                if (self.board[i][j] == self.my_piece):
                    count += 1
        if (count == 4):
            drop_phase = False
        else:
            drop_phase = True

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            nextMove = self.succ(state)
            i, j = 0, 0
            for next in nextMove:
                temp = copy.deepcopy(state)
                temp[next[1][0]][next[1][1]] = ' '
                temp[next[0][0]][next[0][1]] = self.my_piece

                turn = self.max_value(temp, 3)

                if (i < turn):
                    i = turn
                    j = nextMove.index(next)
            turn = nextMove[j]
        else:
            move = []
            nextMove = -100000
            for i in range(5):
                for j in range(5):
                    if (state[i][j] == ' '):
                        temp = copy.deepcopy(state)
                        arr = [(i, j), (i, j)]
                        temp[arr[1][0]][arr[1][1]] = ' '
                        temp[arr[0][0]][arr[0][1]] = self.my_piece

                        ai, opp = 0, 0
                        checkheur = 0
                        if self.game_value(temp) == 1:
                            checkheur = 1
                        if self.game_value(temp) == -1:
                            print(state)
                        for k in range(5):
                            for l in range(5):
                                if (temp[k][l] == self.my_piece):
                                    ai += int(self.weight[k][l])
                                elif (temp[k][l] != ' '):
                                    opp += int(self.weight[k][l])
                        if(checkheur != 1):
                            checkheur = math.sqrt(ai) - math.sqrt(opp)

                        if (nextMove <= checkheur):
                            nextMove = checkheur
                            move = arr
            l = []
            l.append(move[0])
            turn = l
        return turn

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        # ensure the destination (row,col) tuple is at the beginning of the move list

    def succ(self, state):
        piece = self.my_piece
        if(self.game_value(state) == 1 or self.game_value(state) == -1):
            return self.game_value(state)

        possibleMoves = []
        for i in range(5):
            for j in range(5):
                if(state[i][j] == piece):
                    options = self.possibleTreeMoves(i, j, state)

                    for x in options:
                        path = []
                        path.append(x) #possible next move
                        path.append((i,j)) #current spot
                        possibleMoves.append(path)
        return possibleMoves


    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
    def possibleTreeMoves(self, i, j, state):
        possibleMoves = []
        count = 0
        while count < 8:
            if (count == 0 and j < 4 and state[i][j+1]) == ' ': #right
                possibleMoves.append((i, j + 1))
            elif (count == 1 and i < 4 and state[i+1][j]) == ' ': #down
                possibleMoves.append((i + 1, j))
            elif (count == 2 and j > 0 and state[i][j-1]) == ' ': #left
                possibleMoves.append((i, j - 1))
            elif (count == 3 and j > 0 and state[i-1][j]) == ' ': #up
                possibleMoves.append((i-1, j))
            elif (count == 4 and j < 4 and i > 0 and state[i-1][j+1] == ' '): #bottom right
                possibleMoves.append((i-1, j + 1))
            elif (count == 5 and j < 4 and i < 4 and state[i + 1][j+1] == ' '): #top right
                possibleMoves.append((i + 1, j + 1))
            elif (count == 6 and j > 0 and i > 0 and state[i -1][j-1] == ' '): #bottom left
                possibleMoves.append((i - 1, j - 1))
            elif (count == 7 and j > 0 and i < 4 and state[i+1][j-1] == ' '): #bottom right
                possibleMoves.append((i + 1, j - 1))

            count += 1

        return possibleMoves


    def heuristic_game_value(self, state):
        piece = self.my_piece
        ai, opp = 0,0
        if(self.game_value(state) == 1):
            return 1
        if(self.game_value(state) == -1):
            print(state)

        #start evaulating heuristically
        for i in range(5):
            for j in range(5):
                if(state[i][j] != ' '):

                    distance = 0
                    for k in range(5):
                        for l in range(5):
                            if (state[k][l] == piece):
                                distance += math.sqrt((i - k) ** 2 + (j - l) ** 2)
                    distance = math.ceil(distance)

                    if(distance == 0):
                        opp += float(self.weight[i][j])
                    else:
                        opp += float(self.weight[i][j])/3**distance
                elif(state[i][j] == piece):
                    if (distance == 0):
                        ai += float(self.weight[i][j])
                    else:
                        ai += float(self.weight[i][j]) / 4 ** distance
        return math.sqrt(ai) - math.sqrt(opp)

    def max_value(self, state, depth):
        a = -10000000
        b = 10000000
        heurgamevaloriginal = self.heuristic_game_value(state)
        temp = copy.deepcopy(state)
        if(self.game_value(temp) != 0):
            return heurgamevaloriginal
        elif(depth == 0):
            return self.heuristic_game_value(state)
        else:
            nextMoves = self.succ(temp)

            for next in nextMoves:
                temp[next[1][0]][next[1][1]] = ' '
                temp[next[0][0]][next[0][1]] = self.my_piece
                board = temp
                score = self.max_value(board, depth - 1)
                a = a if a >= b else b

                if(score >= heurgamevaloriginal):
                    temp = board
                    heurgamevaloriginal = score

                if(a >= b):
                    break
            return heurgamevaloriginal

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for col in range(3,5):
            for row in range(3,5):
                if state[row][col] != ' ' and state[row-3][col-3] == state[row -2][col-2] == state[row -1][col-1] == state[row][col]:
                    return 1 if state[row][col] == self.my_piece else -1

        # TODO: check / diagonal wins
        for col in range(2):
            for row in range(3,5):
                if state[row][col] != ' ' and state[row-3][col+3] == state[row - 2][col+2] == state[row -1][col+1] == state[row][col]:
                    return 1 if state[row][col] == self.my_piece else -1
        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row][col + 1] == state[row + 1][col] == state[row + 1][col + 1]:
                    return 1 if state[row][col] == self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
