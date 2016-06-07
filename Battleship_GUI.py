import pygame, sys, random

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 200

# Global Variables to be used through our program
win_width = 1400
win_height = 800


# Set up the colours
BLACK = (64, 64, 64)
WHITE = (217, 217, 217)

# Row letters
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

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
    def drawBoards(self, hide, background):
        column_index = '1    2    3    4    5    6    7     8    9   10'
        Surface.fill((0, 0, 0))
        Surface.blit(background, (0, 0))
        text("Computer's Board:" + ' '*36 + "User's Board:" + ' '*37 + 'Round: ' + str(self.round), 75, 25)
        text(column_index + ' '*11 + column_index, 75, 75)
        for x in range(10):
            line = letters[x]
            z = 0
            for y in self.computerBoard[x]:
                if hide:
                    button(' ', 55+(50*z), 105+(40*x), 50, 40, 2, WHITE)
                else:
                    button(y, 55+(50*z), 105+(40*x), 50, 40, 2, WHITE, 'med')
                z += 1
            if x == 8:
                line += ' '*70 + letters[x]
            else:
                line += ' '*68 + letters[x]
            z = 0
            for y in self.userBoard[x]:
                button(y, 622+(50*z), 105+(40*x), 50, 40, 2, WHITE, size='med')
                z += 1
            text(line, 25, 115+(40*x))
        text("Computer's Stats:", 195, 515)
        text("User's Stats:", 760, 515)
        text('Hits              : ' + str(self.hits[0]) + ' '*69 + str(self.hits[1]), 5, 550)
        text('Missess       : ' + str(self.misses[0]) + ' '*69 + str(self.misses[1]), 5, 590)
        text('Ships sunk : ' + str(self.sunk[0][0]) + ' '*69 + str(self.sunk[1][0]), 5, 630)
        button('Save Game', 950, 735, 200, 50, size='med')
        button('Instructions', 1170, 735, 200, 50, size='med')

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

    # Checks to see if a ship was sunk
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
                    # Finds the probability for each cell based on a PDF
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


def instructions(background):
    Surface.fill((0, 0, 0))
    Surface.blit(background, (0, 0))
    title("Instructions", win_width/2 - 200, 25)
    text("Use the mouse to position your ship and press space bar to flip the orientation.", 150, 115)
    text("Ships cannot overlap or go outside the bounds of the grid.", 255, 155)
    title("Fleet", win_width/2 - 100, 200)
    text("A = Aircraft Carrier (5 units)", 300, 290)
    text("# = Hit on a ship", 775, 290)
    text("B = Battleship (4 units)", 300, 330)
    text("*  = Miss", 777, 330)
    text("D = Destroyer (3 units)", 300, 370)
    text("S = Submarine (3 units)", 300, 410)
    text("P = Patrol Boat (2 units)", 300, 450)
    button('Return to game', 1070, 735, 300, 50, size='med')


def title(msg, x, y):
    title = title_font.render(msg, True, WHITE)
    result_rect = title.get_rect()
    result_rect.topleft = (x, y)
    Surface.blit(title, result_rect)


def text(msg, x, y):
    text = text_font.render(msg, True, WHITE)
    result_rect = text.get_rect()
    result_rect.topleft = (x, y)
    Surface.blit(text, result_rect)


def home_screen():
    title('Battleship', win_width/2 - 200, 25)
    image = pygame.image.load('pieces.png')
    Surface.blit(image, ((win_width/2) - 450, 110))
    button('New Game', (win_width/2) - 150, 375, 300, 50)
    button('Load Game', (win_width/2) - 150, 450, 300, 50)


def button(msg, x, y, w, h, border=0, color=BLACK, size='lrg'):
    pygame.draw.rect(Surface, (115, 115, 115), (x, y, w, h), border)
    if size == 'lrg':
        text_surf = button_font.render(msg, True, color)
    else:
        text_surf = text_font.render(msg, True, color)
    result_rect = text_surf.get_rect()
    result_rect.center = ((x + (w/2)), (y + (h/2)))
    Surface.blit(text_surf, result_rect)

def new_game():
    title('Please select a difficulty', win_width/2 - 425, 100)
    button('Easy', (win_width/2) - 175, 250, 300, 50)
    button('Medium', (win_width/2) - 175, 325, 300, 50)
    button('Hard', (win_width/2) - 175, 400, 300, 50)

def main():
    # Initialize the board and all the placements of ships
    board = BattleshipGame()
    board.comupterPlace()
    pygame.init()
    global Surface

    # Font info
    global title_font, button_font, text_font
    title_font = pygame.font.Font('freesansbold.ttf', 70)
    button_font = pygame.font.Font('freesansbold.ttf', 40)
    text_font = pygame.font.Font('freesansbold.ttf', 30)

    # Initialize GUI settings
    FPS_clock = pygame.time.Clock()
    Surface = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('Battleship')
    pygame.display.set_icon(pygame.image.load('Ticonderoga_cruiser.gif'))
    background = pygame.transform.scale(pygame.image.load('water.png'), (win_width, win_height))
    background.set_alpha(150)
    Surface.blit(background, (0, 0))

    # Display the home screen
    home_screen()
    screen = 0
    diff = 0

    while True:
        # Main event loop
        for event in pygame.event.get():
            # Quits the game and closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if screen == 0:
                    if ((win_width/2) - 150) + 300 > pygame.mouse.get_pos()[0] > ((win_width/2) - 150) \
                            and 425 > pygame.mouse.get_pos()[1] > 375:
                        print('New Game')
                        Surface.fill((0, 0, 0))
                        Surface.blit(background, (0, 0))
                        new_game()
                        screen = 1
                    elif ((win_width/2) - 150) + 300 > pygame.mouse.get_pos()[0] > ((win_width/2) - 150) \
                            and 500 > pygame.mouse.get_pos()[1] > 450:
                        print('Load Game')
                elif screen == 1:
                    if ((win_width/2) - 175) + 300 > pygame.mouse.get_pos()[0] > ((win_width/2) - 175) \
                            and 300 > pygame.mouse.get_pos()[1] > 250:
                        diff = 1
                        screen = 2
                    elif ((win_width/2) - 175) + 300 > pygame.mouse.get_pos()[0] > ((win_width/2) - 175) \
                            and 375 > pygame.mouse.get_pos()[1] > 325:
                        diff = 2
                        screen = 2
                    elif ((win_width/2) - 175) + 300 > pygame.mouse.get_pos()[0] > ((win_width/2) - 175) \
                            and 450 > pygame.mouse.get_pos()[1] > 400:
                        diff = 3
                        screen = 2
                elif screen == 2:
                    if 1370 > pygame.mouse.get_pos()[0] > 1170 and 785 > pygame.mouse.get_pos()[1] > 735:
                        instructions(background)
                        screen = 3
                elif screen == 3:
                    if 1370 > pygame.mouse.get_pos()[0] > 1070 and 785 > pygame.mouse.get_pos()[1] > 735:
                        screen = 2


        if screen == 2:
            board.drawBoards(False, background)

        # Updates the display
        pygame.display.update()
        FPS_clock.tick(FPS)

if __name__ == '__main__':
    main()