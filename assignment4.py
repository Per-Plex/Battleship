__author__ = 'Ceegan'

import random


class BattleshipGame():
    def __init__(self):
        self.userBoard = [[' ' for x in range(10)] for x in range(10)]
        self.computerBoard = [[' ' for x in range(10)] for x in range(10)]
        self.userShips = {'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2}
        self.computerShips = {'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2}
        self.reference = {'A': 'Aircraft Carrier', 'B': 'Battleship', 'S': 'Submarine', 'D': 'Destroyer', 'P': 'Patrol Boat'}

    # Displays the board
    def drawBoards(self, hide):
        numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        line = "    Computer's board:         User's board:\n    " + '%s '*10 % numbers + '     ' + '%d '*10 % numbers \
               + '\n'
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for x in range(10):
            line += ' ' + letters[x] + ' '
            for y in self.computerBoard[x]:
                # Displays the ships if hide is true
                if hide:
                    if y == 'A' or y == 'B' or y == 'S' or y == 'D' or y == 'P':
                        line += '| '
                    else:
                        line += '|' + y
                else:
                    line += '|' + y
            line += '|   ' + letters[x] + ' |' + '|'.join(self.userBoard[x]) + '|\n'
        print(line)

    # Validates placement of the ships when placing
    def validatePlacement(self, computer, size, x, y, orientation):
        # Assigns the board to be iterated through based on the var computer
        if computer:
            board = self.computerBoard
        else:
            board = self.userBoard

        for z in range(size):
            if orientation == 'v':
                if board[x+z][y] != ' ':
                    return False
            else:
                if board[x][y+z] != ' ':
                    return False
        return True

    # Places the computers ships at random locations and orientations
    def comupterPlace(self):
        for x in self.computerShips:
            # choose the orientation
            orientation = random.choice(['v', 'h'])
            valid = False

            # validates the placement
            while not valid:
                x_axis = random.randint(0, 9)
                y_axis = random.randint(0, 9)
                if orientation == 'v' and x_axis+self.computerShips[x] < 9:
                    valid = self.validatePlacement(True, self.computerShips[x], x_axis, y_axis, orientation)
                if orientation == 'h' and y_axis+self.computerShips[x] < 9:
                    valid = self.validatePlacement(True, self.computerShips[x], x_axis, y_axis, orientation)

            # Places the ship
            for y in range(self.computerShips[x]):
                if orientation == 'v':
                    self.computerBoard[x_axis+y][y_axis] = x
                else:
                    self.computerBoard[x_axis][y_axis+y] = x

    # Places the user ships
    def userPlace(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for x in self.userShips:
            valid = False

            # Loops through till valid place is chosen
            while not valid:
                orientation = 'n'
                number = False
                coordinates = ['Z', None]
                print('Placing a ' + self.reference[x] + ' of size ' + str(self.userShips[x]))

                # Validates the input
                while coordinates[0] not in letters or not number:
                    coordinates = input('Enter coordinates x y (x in [A..J] and y in [1..10]): ').split(' ')
                    try:
                        if len(coordinates) > 1:
                            coordinates[1] = int(coordinates[1])
                            if coordinates[1] > 10 or coordinates[1] < 1:
                                raise ValueError
                        else:
                            raise ValueError
                    except ValueError:
                        pass
                    else:
                        number = True

                # Validates the orientation
                while orientation != 'v' and orientation != 'h':
                    orientation = input('Is this ship vertical or horizontal (v,h)? ').lower()
                x_axis = letters.index(coordinates[0])
                y_axis = coordinates[1]-1

                # Checks to make sure the coordinates are valid
                if orientation == 'v' and x_axis + self.userShips[x] < 9:
                    valid = self.validatePlacement(False, self.userShips[x], x_axis, y_axis, orientation)
                elif orientation == 'h' and y_axis + self.userShips[x] < 9:
                    valid = self.validatePlacement(False, self.userShips[x], x_axis, y_axis, orientation)

                # Error message
                if not valid:
                    input('Cannot place a ' + self.reference[x] +
                          ' there. Either the stern is out of the board or collides it with another ship.\nPlease take '
                          'a look at the board and try again.\nHit ENTER to continue\n')
                # Places the ship
                else:
                    for y in range(self.userShips[x]):
                        if orientation == 'v':
                            self.userBoard[x_axis+y][y_axis] = x
                        else:
                            self.userBoard[x_axis][y_axis+y] = x
                    self.drawBoards(True)

    # Gets all the sunk and to be sunk ships
    def getEnemyFleet(self, computer):
        line = 'Ships to sink:'
        sink = []
        sunk = []
        if computer:
            ships = self.userShips
        else:
            ships = self.computerShips
        for x in ships:
            if ships[x] != 0:
                sink.append(self.reference[x])
            else:
                sunk.append(self.reference[x])
        line += '['
        for x in sink:
            line += x + ' '

        line += '] Ships sunk:['
        for x in sunk:
            line += x + ' '
        line += ']'
        print(line)

    # Checks to see if you have won
    def checkWinning(self, computer):
        if computer:
            ships = self.computerShips
        else:
            ships = self.userShips
        for x in ships:
            if ships[x] != 0:
                return False
        return True

    # Makes a move on the opposite board
    def makeA_Move(self, computer, x, y):
        # Assigns the board to place the move
        if computer:
            board = self.userBoard
        else:
            board = self.computerBoard
        sunk = False
        # Checks id you already made a move there
        if board[x][y] == '*' or board[x][y] == '#':
            return board[x][y]
        else:
            # Gets the old symbol in that cell
            old = board[x][y]
            # If a ship was in that cell
            if board[x][y] != ' ':
                board[x][y] = '#'
                # Checks to see if you sunk the ship
                sunk = self.checkIfSunk(computer, old)
            else:
                board[x][y] = '*'
            # returns the old cell symbol and if you sunk a ship
            return old, sunk

    # Checks if you sunk a ship
    def checkIfSunk(self, computer, ship):
        if computer:
            ships = self.computerShips
        else:
            ships = self.userShips
        ships[ship] -= 1
        return ships[ship] == 0


def main():
    # Initialize the board and all the placements of ships
    board = BattleshipGame()
    board.comupterPlace()
    board.drawBoards(True)
    board.userPlace()
    player = True
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    # Loop till someone wins
    while not board.checkWinning(player):
        number = False
        content = ['*', None]
        coordinates = ['Z', None]
        # If its the players turn
        if player:
            board.drawBoards(True)
            board.getEnemyFleet(player)
            # Error trap till correct input
            while coordinates[0] not in letters or not number:
                    coordinates = input('Enter coordinates x y (x in [A..J] and y in [1..10]): ').split(' ')
                    try:
                        if len(coordinates) > 1:
                            coordinates[1] = int(coordinates[1])
                            if coordinates[1] > 10 or coordinates[1] < 1:
                                raise ValueError
                        else:
                            raise ValueError
                    except ValueError:
                        pass
                    else:
                        number = True
        else:
            coordinates = [random.choice(letters), random.randint(1, 10)]
        # Makes a move to the board
        while content[0] == '*' or content[0] == '#':
            content = board.makeA_Move(not player, letters.index(coordinates[0]), coordinates[1]-1)
            coordinates[1] = str(coordinates[1])
            # Message if you already chose that cell
            if content[0] == '*' or content[0] == '#':
                if player:
                    print('Sorry, ' + coordinates[0] + ' ' + coordinates[1] + ' was already played. Try again.')
                else:
                    coordinates = [random.choice(letters), random.randint(1, 10)]
        # Different messages based on if you hit or missed
        if player:
            if content[0] == ' ':
                print('Sorry, ' + coordinates[0] + ' ' + coordinates[1] + ' is a miss')
            else:
                print('Hit at ' + coordinates[0] + ' ' + coordinates[1])
        else:
            if content[0] == ' ':
                print('Computer missed at ' + coordinates[0] + ' ' + coordinates[1] + '\n')
            else:
                print('Computer did a hit at ' + coordinates[0] + ' ' + coordinates[1] + '\n')
        if content[1]:
                    print(board.reference[content[0]] + ' sunk')
        # Flips the player
        player = not player
    # End game messages
    if player:
        print('Congratulations! User WON!')
    else:
        print('Sorry, you lost')

if __name__ == '__main__':
    main()