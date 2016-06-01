__author__ = 'Ceegan'

import random
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
possible_positions = []

class BattleshipGame():
    def __init__(self):
        self.userBoard = [[' ' for x in range(10)] for x in range(10)]
        self.computerBoard = [[' ' for x in range(10)] for x in range(10)]
        self.userShips = {'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2}
        self.computerShips = {'A': 5, 'B': 4, 'S': 3, 'D': 3, 'P': 2}
        self.reference = {'A': ['Aircraft Carrier', 5], 'B': ['Battleship', 4], 'S': ['Submarine', 3],
                          'D': ['Destroyer', 3], 'P': ['Patrol Boat', 2]}
        self.round = 0
        self.hits = [0, 0]
        self.misses = [0, 0]
        self.sunk = [[0, None, None, None, None, None], [0, None, None, None, None, None]]

    # Displays the board
    def drawBoards(self, hide):
        z = 1
        done = False
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

            # Displays the number of hits
            if x == 0:
                line += 'Nbr. of hits  :  %s' % self.hits[0]
                if self.hits[0] < 10:
                    line += ' '*17
                else:
                    line += ' '*16
                line += '%s\n' % self.hits[1]

            # Displays the number of misses
            elif x == 1:
                line += 'Nbr. of misses:  %s' % self.misses[0]
                if self.misses[0] < 10:
                    line += ' '*17
                else:
                    line += ' '*16
                line += '%s\n' % self.misses[1]

            # Displays the number of ships sunk
            elif x == 2:
                line += 'Ships sunk    :  %s' % self.sunk[0][0] + ' '*17 + '%s\n' % self.sunk[1][0]

            # Displays the ships sunk
            elif self.sunk[0][1] or self.sunk[1][1]:
                if z < 6:
                    if not self.sunk[0][z] and self.sunk[1][z]:
                        line += ' '*35 + '%s\n' % self.sunk[1][z]
                        z += 1
                    elif self.sunk[0][z] and self.sunk[1][z]:
                        line += ' '*17 + '%s' % self.sunk[0][z] + ' '*(18-len(self.sunk[0][z])) + '%s\n' % self.sunk[1][z]
                        z += 1
                    elif self.sunk[0][z] and not self.sunk[1][z]:
                        line += ' '*17 + '%s\n' % self.sunk[0][z]
                        z += 1
                    else:
                        line += '\n'
                else:
                    line += '\n'
            else:
                line += '\n'
        print(line)
        #print(self.sunk)

    # Validates placement of the ships when placing
    def validatePlacement(self, computer, size, x, y, orientation):

        # Assigns the board to be iterated through based on the var computer
        if computer:
            board = self.computerBoard
        else:
            board = self.userBoard

        # Validates the placement
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
                if orientation == 'v' and x_axis+self.computerShips[x] < 11:
                    valid = self.validatePlacement(True, self.computerShips[x], x_axis, y_axis, orientation)
                if orientation == 'h' and y_axis+self.computerShips[x] < 11:
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
                print('Placing a ' + self.reference[x][0] + ' of size ' + str(self.userShips[x]))

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
                if orientation == 'v' and x_axis + self.userShips[x] < 11:
                    valid = self.validatePlacement(False, self.userShips[x], x_axis, y_axis, orientation)
                elif orientation == 'h' and y_axis + self.userShips[x] < 11:
                    valid = self.validatePlacement(False, self.userShips[x], x_axis, y_axis, orientation)

                # Error message
                if not valid:
                    input('Cannot place a ' + self.reference[x][0] +
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
                sink.append(self.reference[x][0])
            else:
                sunk.append(self.reference[x][0])
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

                        # Adds the sunk ship to the first empty spot
                        while self.sunk[0][z]:
                            z += 1
                        self.sunk[0][z] = self.reference[old][0]
                else:
                    self.hits[1] += 1
                    if sunk:
                        self.sunk[1][0] += 1
                        z = 1

                        # Adds the sunk ship to the first empty spot
                        while self.sunk[1][z]:
                            z += 1
                        self.sunk[1][z] = self.reference[old][0]
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

    # Increments the game rounds
    def incrementRounds(self):
        self.round += 1

    # Checks ahead and behind the current cell to see if there is a limit
    def check_ahead_behind(self, x, y, size):
        limit = [[5, 5], [5, 5]]
        found = [False, False, False, False]
        over = [False, False, False, False]
        for z in range(1, size):
            if x - z >= 0:
                if (self.userBoard[y][x-z] == '*' or self.userBoard[y][x-z] == "#") and not found[0]:
                    limit[0][1] = z
                    found[0] = True
            elif not over[0] and not found[0]:
                limit[0][1] = z
                over[0] = True
            if x + z <= 9:
                if (self.userBoard[y][x+z] == '*' or self.userBoard[y][x+z] == "#") and not found[1]:
                    limit[0][0] = z
                    found[1] = True
            elif not over[1] and not found[1]:
                limit[0][0] = z
                over[1] = True
            if y - z >= 0:
                if (self.userBoard[y-z][x] == "*" or self.userBoard[y-z][x] == "#") and not found[2]:
                    limit[1][1] = z
                    found[2] = True
            elif not over[2] and not found[2]:
                limit[1][1] = z
                over[2] = True
            if y + z <= 9:
                if (self.userBoard[y+z][x] == "*" or self.userBoard[y+z][x] == "#") and not found[3]:
                    limit[1][0] = z
                    found[3] = True
            elif not over[3] and not found[3]:
                limit[1][0] = z
                over[3] = True

        return limit

    # Makes the move for the computer
    def AI_move(self, coordinates, target, diff):
        global possible_positions
        if diff == "1":
            coordinates = [letters.index(random.choice(letters)), random.randint(0, 9)]
        else:
            # Converts the number back into int from a str because of displaying
            coordinates[1] = int(coordinates[1])

            # Searches the board for a ship
            if not target:
                possible_positions = []
                if diff == "2":
                    coordinates[1] += 2

                    # Bumps its search down a row
                    if coordinates[1] == 10:
                        coordinates = [coordinates[0] + 1, coordinates[1]-9]
                    elif coordinates[1] == 11:
                        coordinates = [coordinates[0] + 1, coordinates[1]-11]

                    # Coming back from target mode into hunt mode
                    while self.userBoard[coordinates[0]][coordinates[1]] == '#' or\
                                    self.userBoard[coordinates[0]][coordinates[1]] == '*':
                        coordinates[1] += 2
                        if coordinates[1] == 10:
                            coordinates = [coordinates[0] + 1, coordinates[1]-9]
                        elif coordinates[1] == 11:
                            coordinates = [coordinates[0] + 1, coordinates[1]-11]
                else:
                    possiblelocation = [[0 for x in range(10)] for x in range(10)]
                    largest = 0
                    available_cells = [-1, -1]
                    available_ships = []
                    for key in self.userShips:
                        available_ships.append(self.userShips[key])
                        if self.userShips[key] > largest:
                            largest = self.userShips[key]
                    # Finds the PDF for each cell
                    for y in range(10):
                        for x in range(10):
                            if self.userBoard[y][x] == "*" or self.userBoard[y][x] == "#":
                                possiblelocation[y][x] = 0
                            else:
                                limit = self.check_ahead_behind(y, x, largest)
                                available_cells = [(limit[0][0] + limit[0][1]) - 1, (limit[1][0] + limit[1][1]) - 1]
                                for ship in available_ships:
                                    for orientation in range(2):
                                        if ship == available_cells[orientation]:
                                            possiblelocation[y][x] += 1
                                        elif limit[orientation][1] < limit[orientation][0]:
                                            if available_cells[orientation] >= ship:
                                                if ship >= limit[orientation][1]:
                                                    possiblelocation[y][x] += limit[orientation][1]
                                                else:
                                                    possiblelocation[y][x] += ship
                                        elif limit[orientation][0] < limit[orientation][1]:
                                            if available_cells[orientation] >= ship:
                                                if ship >= limit[orientation][0]:
                                                    possiblelocation[y][x] += limit[orientation][0]
                                                else:
                                                    possiblelocation[y][x] += ship
                                        else:
                                            if available_cells[orientation] >= ship:
                                                if ship <= limit[orientation][0]:
                                                    possiblelocation[y][x] += ship
                                                else:
                                                    possiblelocation[y][x] += (available_cells[orientation] - ship) + 1
                    biggest = [[0, 0, 0]]
                    for y in range(10):
                        for x in range(10):
                            if possiblelocation[y][x] > biggest[0][0]:
                                biggest[0] = [possiblelocation[y][x], y, x]
                    #for x in possiblelocation:
                     #   print(x)
                    coordinates = [biggest[0][1], biggest[0][2]]

            else:
                # Appends the possible hit position (N, E, S, W)
                if coordinates[0] - 1 >= 0 and self.userBoard[coordinates[0] - 1][coordinates[1]] != '#' and\
                                self.userBoard[coordinates[0] - 1][coordinates[1]] != '*' and\
                                [coordinates[0] - 1, coordinates[1]] not in possible_positions:
                    possible_positions.append([coordinates[0] - 1, coordinates[1]])
                if coordinates[1] + 1 < 10 and self.userBoard[coordinates[0]][coordinates[1] + 1] != '#' and\
                                self.userBoard[coordinates[0]][coordinates[1] + 1] != '*' and\
                                [coordinates[0], coordinates[1] + 1] not in possible_positions:
                    possible_positions.append([coordinates[0], coordinates[1] + 1])
                if coordinates[0] + 1 < 10 and self.userBoard[coordinates[0] + 1][coordinates[1]] != '#' and\
                                self.userBoard[coordinates[0] + 1][coordinates[1]] != '*' and\
                                [coordinates[0] + 1, coordinates[1]] not in possible_positions:
                    possible_positions.append([coordinates[0] + 1, coordinates[1]])
                if coordinates[1] - 1 >= 0 and self.userBoard[coordinates[0]][coordinates[1] - 1] != '#' and\
                                self.userBoard[coordinates[0]][coordinates[1] - 1] != '*' and\
                                [coordinates[0], coordinates[1] - 1] not in possible_positions:
                    possible_positions.append([coordinates[0], coordinates[1] - 1])
                print(possible_positions)
                # Pops the last append position for the AI to hit
                coordinates = possible_positions.pop()
        return coordinates

def main():
    diff = 0
    welcome = """
 __      __       .__                                  __           __________         __    __  .__                .__    .__
/  \    /  \ ____ |  |   ____  ____   _____   ____   _/  |_  ____   \______   \_____ _/  |__/  |_|  |   ____   _____|  |__ |__|_____
\   \/\/   // __ \|  | _/ ___\/  _ \ /     \_/ __ \  \   __\/  _ \   |    |  _/\__  \\\   __\   __\  | _/ __ \ /  ___/  |  \|  \____ \\
 \        /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/   |  | (  <_> )  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   Y  \  |  |_> >
  \__/\  /  \___  >____/\___  >____/|__|_|  /\___  >  |__|  \____/   |______  /(____  /__|  |__| |____/\___  >____  >___|  /__|   __/
       \/       \/          \/            \/     \/                         \/      \/                     \/     \/     \/   |__|
"""
    print(welcome)
    while diff != "1" and diff != "2" and diff != "3":
        diff = input("\nPlease select a difficulty:\n1. Easy   (AI randomly shoots)\n2. Medium (AI uses hunt"
              ", with parity, and target)\n3. Hard   (AI uses hunt, witgh PDF algorthim, and target)\n\n>")


    # Initialize the board and all the placements of ships
    board = BattleshipGame()
    board.comupterPlace()
    board.drawBoards(True)
    board.userPlace()
    player = True
    AI_coordinates = [0, -1]
    target = False
    hits = 0
    global possible_positions

    # Loop till someone wins
    while not board.checkWinning(player):
        number = False
        content = ['*', None]

        # Makes a move to the board
        while content[0] == '*' or content[0] == '#':
            if player:
                coordinates = ['Z', None]
                if board.round != 0:
                    board.drawBoards(False)

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

                # Calls the move for the AI
                coordinates = board.AI_move(AI_coordinates, target, diff)
                AI_coordinates = coordinates

                content = board.makeA_Move(True, coordinates[0], coordinates[1])
            coordinates[1] = str(coordinates[1])

            # Message if you already chose that cell
            if (content[0] == '*' or content[0] == '#') and player:
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

                # If its most recent hit was a miss goes back to the last hit cell
                if target:
                    AI_coordinates = recent_hit

                    # If there are no more possible positions to hit from its current cell
                    # goes back to where it first hit
                    if len(possible_positions) == 0:
                        AI_coordinates = first_hit
            else:
                print('Computer did a hit at ' + letters[coordinates[0]] + ' %s' % (int(coordinates[1]) + 1) + '')
                # Turns target mode on
                target = True

                # Saves the first hit
                if hits == 0:
                    first_hit = coordinates

                # Saves the most resent hit
                recent_hit = coordinates

                # Clears the possible positions and increments the hits
                #possible_positions = []
                hits += 1

        # If a ship was sunk
        if content[1]:
            if not player:

                # Checks to see if the hits equals the length of the ship sunk
                if hits != board.reference[content[0]][1]:
                    hits = 1
                else:
                    target = False
                    hits = 0

                # Resets the AI position back to where it first made a hit
                AI_coordinates = first_hit
                #possible_positions = []
            if player:
                print("You've sunk the enemy %s" % board.reference[content[0]][0])
            else:
                print("The enemy has sunk our %s " % board.reference[content[0]][0])
            input('Press RETURN to continue\n')
        # Flips the player
        player = not player
    # End game messages
    board.drawBoards(False)
    if not player:
        print('Congratulations! User WON!')
    else:
        print('Sorry, the enemy has sunk your fleet')

if __name__ == '__main__':
    main()
