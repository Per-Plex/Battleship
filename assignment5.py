__author__ = 'Ceegan'

import random
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
possible_directions = ['N', 'E', 'S', 'W']
possible_positions = []

class BattleshipGame():
    def __init__(self):
        self.userBoard = [[' ' for x in range(10)] for x in range(10)]
        self.computerBoard = [[' ' for x in range(10)] for x in range(10)]
        self.userShips = {'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2}
        self.computerShips = {'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2}
        self.reference = {'A': 'Aircraft Carrier', 'B': 'Battleship', 'S': 'Submarine', 'D': 'Destroyer',
                          'P': 'Patrol Boat'}
        self.round = 0
        self.hits = [0, 0]
        self.misses = [0, 0]
        self.sunk = [[0, None, None, None, None, None], [0, None, None, None, None, None]]

    # Displays the board
    def drawBoards(self, hide):
        z = 1
        numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        line = "    Computer's board:         User's board:         at round: %s" % self.round + "\n    " + \
               '%s '*10 % numbers + '     ' + '%d '*10 % numbers + ' '*18 + 'Computer Status:  User Status:\n'
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
            line += '|   ' + letters[x] + ' |' + '|'.join(self.userBoard[x]) + '|  '
            if x == 0:
                line += 'Nbr. of hits  :  %s' % self.hits[0]
                if self.hits[0] < 10:
                    line += ' '*17
                else:
                    line += ' '*16
                line += '%s\n' % self.hits[1]
            elif x == 1:
                line += 'Nbr. of misses:  %s' % self.misses[0]
                if self.misses[0] < 10:
                    line += ' '*17
                else:
                    line += ' '*16
                line += '%s\n' % self.misses[1]
            elif x == 2:
                line += 'Ships sunk    :  %s' % self.sunk[0][0] + ' '*17 + '%s\n' % self.sunk[1][0]
            elif self.sunk[0][1] or self.sunk[1][1]:
                if not self.sunk[0][z] and self.sunk[1][z]:
                    line += ' '*35 + '%s\n' % self.sunk[1][z]
                    z += 1
                elif self.sunk[0][z] and self.sunk[1][z]:
                    line += ' '*17 + '%s' % self.sunk[0][z] + ' '*(18-len(self.sunk[0][z])) + '%s\n' % self.sunk[1][z]
                    z += 1
                else:
                    line += '\n'
            else:
                line += '\n'
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
            self.round += 1
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
                if computer:
                    self.hits[0] += 1
                    if sunk:
                        self.sunk[0][0] += 1
                        z = 1
                        while self.sunk[0][z]:
                            z += 1
                        print(z)
                        self.sunk[0][z] = self.reference[old]
                else:
                    self.hits[1] += 1
                    if sunk:
                        self.sunk[1][0] += 1
                        z = 1
                        while self.sunk[1][z]:
                            z += 1
                        self.sunk[1][z] = self.reference[old]
            else:
                board[x][y] = '*'
                if computer:
                    self.misses[0] += 1
                else:
                    self.misses[1] += 1
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

    def incrementRounds(self):
        self.round += 1

    def getHits(self, computer):
        if computer:
            return self.hits[0]
        return self.hits[1]

    def getMisses(self, computer):
        if computer:
            return self.hits[0]
        return self.hits[1]

    def AI_move(self, coordinates, target, content):
        if type(coordinates[0]) != int:
            coordinates[0] = letters.index(coordinates[0])
        coordinates[1] = int(coordinates[1])
        if not target:
            coordinates[1] += 2
            if coordinates[1] == 12:
                coordinates = [coordinates[0] + 1, coordinates[1]-11]
            elif coordinates[1] == 11:
                coordinates = [coordinates[0] + 1, coordinates[1]-9]
            while self.userBoard[coordinates[0]][coordinates[1]] == '#' or self.userBoard[coordinates[0]][coordinates[1]] == '*':
                coordinates[1] += 2
                if coordinates[1] == 12:
                    coordinates = [coordinates[0] + 1, coordinates[1]-11]
                elif coordinates[1] == 11:
                    coordinates = [coordinates[0] + 1, coordinates[1]-9]
        else:
            if coordinates[0] - 1 >= 0 and self.userBoard[coordinates[0] - 1][coordinates[1]] != '#' and self.userBoard[coordinates[0] - 1][coordinates[1]] != '*':
                possible_positions.append([coordinates[0] - 1, coordinates[1]])
            if coordinates[1] + 1 < 10 and self.userBoard[coordinates[0]][coordinates[1] + 1] != '#' and self.userBoard[coordinates[0]][coordinates[1] + 1] != '*':
                possible_positions.append([coordinates[0], coordinates[1] + 1])
            if coordinates[0] + 1 < 10 and self.userBoard[coordinates[0] + 1][coordinates[1]] != '#' and self.userBoard[coordinates[0] + 1][coordinates[1]] != '*':
                possible_positions.append([coordinates[0] + 1, coordinates[1]])
            if coordinates[1] - 1 >= 0 and self.userBoard[coordinates[0]][coordinates[1] - 1] != '#' and self.userBoard[coordinates[0]][coordinates[1] - 1] != '*':
                possible_positions.append([coordinates[0], coordinates[1] - 1])
            print(possible_positions)
            coordinates = possible_positions.pop()
        print(coordinates)
        return coordinates

def main():
    # Initialize the board and all the placements of ships
    board = BattleshipGame()
    board.comupterPlace()
    board.drawBoards(True)
    board.userPlace()
    player = True
    AI_coordinates = [0, -1]
    target = False
    hits = 0
    global possible_positions, possible_directions
    # Loop till someone wins
    while not board.checkWinning(player):
        number = False
        content = ['*', None]

        # Makes a move to the board
        while content[0] == '*' or content[0] == '#':
            if player:
                coordinates = ['Z', None]
                board.drawBoards(False)
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
                content = board.makeA_Move(False, letters.index(coordinates[0]), int(coordinates[1])-1)
            else:
                coordinates = board.AI_move(AI_coordinates, target, content[0])
                AI_coordinates = coordinates
                content = board.makeA_Move(True, coordinates[0], coordinates[1])
            coordinates[1] = str(coordinates[1])
            # Message if you already chose that cell
            if content[0] == '*' or content[0] == '#':
                if player:
                    print('Sorry, ' + coordinates[0] + ' ' + coordinates[1] + ' was already played. Try again.\n')
        # Different messages based on if you hit or missed
        if player:
            if content[0] == ' ':
                print('Sorry, ' + coordinates[0] + ' ' + coordinates[1] + ' is a miss')
            else:
                print('Hit at ' + coordinates[0] + ' ' + coordinates[1])
        else:
            if content[0] == ' ':
                print('Computer missed at ' + letters[coordinates[0]] + ' %s' % (int(coordinates[1]) + 1) + '\n')
                if target:
                    possible_directions.pop()
                    print(possible_directions)
                    AI_coordinates = recent_hit
                    print(possible_directions)
                    if len(possible_positions) == 0:
                        AI_coordinates = first_hit
            else:
                print('Computer did a hit at ' + letters[coordinates[0]] + ' %s' % (int(coordinates[1]) + 1) + '\n')
                target = True
                if hits == 0:
                    first_hit = coordinates
                recent_hit = coordinates
                possible_positions = []
                hits += 1
        if content[1]:
            if not player:
                if content[0] == 'A':
                    length = 5
                elif content[0] == 'B':
                    length = 4
                elif content[0] == 'D':
                    length = 3
                elif content[0] == 'S':
                    length = 3
                else:
                    length = 2
                if hits != length:
                    possible_directions.pop()
                    hits = 1
                else:
                    target = False
                    hits = 0
                    possible_directions = ['N', 'E', 'S', 'W']
                AI_coordinates = first_hit

                possible_positions = []
            input(board.reference[content[0]] + ' sunk\nPress RETURN to continue')
        # Flips the player
        player = not player
    # End game messages
    if not player:
        print('Congratulations! User WON!')
    else:
        print('Sorry, you lost')

if __name__ == '__main__':
    main()