import pygame, sys, random, copy, ast

# Number of frames per second
# Change this value to speed up or slow down the game
FPS = 200

# Width and height of the window
win_width = 1400
win_height = 800


# Set up the colours
BLACK = (64, 64, 64)
WHITE = (217, 217, 217)

# Row letters
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Stores Button objects
buttons = []

# Difficulty
diff = 0

# Boolean for if the user/load finished placing their/the ships
placed = False


class BattleshipGame:
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
    def draw_main_screen(self, hide):
        delete_buttons()
        column_index = '1    2    3    4    5    6    7     8    9   10'
        Surface.fill((0, 0, 0))
        Surface.blit(background, (0, 0))
        text("Computer's Board:" + ' '*36 + "User's Board:" + ' '*37 + 'Round: ' + str(self.round), 75, 25, 'med')
        text(column_index + ' '*11 + column_index, 75, 75, 'med')
        for x in range(10):
            write_obj = letters[x]
            z = 0
            for y in range(10):
                if hide:
                    Button(' ', 55+(50*z), 105+(40*x), 50, 40, 'board.makeA_Move(False, %s, %d)' %
                           (x, y), border=2, color=WHITE, size='med')
                else:
                    Button(self.computerBoard[x][y], 55+(50*z), 105+(40*x), 50, 40, 'board.makeA_Move(False, %s, %d)' %
                           (x, y), border=2, color=WHITE, size='med')
                z += 1
            if x == 8:
                write_obj += ' '*70 + letters[x]
            else:
                write_obj += ' '*68 + letters[x]
            z = 0
            for y in self.userBoard[x]:
                Button(y, 622+(50*z), 105+(40*x), 50, 40, 'None', border=2, color=WHITE, size='med')
                z += 1
            text(write_obj, 25, 115+(40*x), 'med')
        if len(messages) >= 21:
            for x in range(len(messages) - 20):
                messages.pop()
        for x in range(len(messages) - 1):
            if x % 2 == 0:
                text(messages[x], 1130, 490-(x*20), 'sml')
            else:
                text(messages[x], 1130, 490-(x*20), 'sml', color=(153, 153, 153))
        text("Computer's Stats:", 195, 515, 'med')
        text("User's Stats:", 760, 515, 'med')

        # Spacing for hits and misses
        if self.misses[0] > 9:
            Mspace = 67
        else:
            Mspace = 69
        if self.hits[0] > 9:
            Hspace = 67
        else:
            Hspace = 69

        text('Hits              : ' + str(self.hits[0]) + ' '*Hspace + str(self.hits[1]), 5, 550, 'med')
        text('Missess       : ' + str(self.misses[0]) + ' '*Mspace + str(self.misses[1]), 5, 590, 'med')
        text('Ships sunk : ' + str(self.sunk[0][0]) + ' '*69 + str(self.sunk[1][0]), 5, 630, 'med')
        Button('Save Game', 1170, 735, 200, 50, 'board.save_game()', size='med')

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

    # Draws the screen where the user places their ships
    @staticmethod
    def draw_user_place_screen(user_board):
        Surface.fill((0, 0, 0))
        Surface.blit(background, (0, 0))
        text('Place Your Fleet', win_width/2 - 270, 25, 'lrg')
        text("Use the arrow keys to position your ship, press space bar to flip the orientation,", 135, 115, 'med')
        text("and enter to place the ship on the board. Ships cannot overlap or go outside the", 135, 155, 'med')
        text("bounds of the grid.", 135, 195, 'med')
        for x in range(10):
            z = 0
            for y in user_board[x]:
                Button(y, 100+(50*z), 235+(40*x), 50, 40, 'None', border=2, color=WHITE, size='med')
                z += 1
        text("Fleet", 900, 235, 'lrg')
        text("A = Aircraft Carrier (5 units)", 750, 325, 'med')
        text("B = Battleship (4 units)", 750, 365, 'med')
        text("D = Destroyer (3 units)", 750, 405, 'med')
        text("S = Submarine (3 units)", 750, 445, 'med')
        text("P = Patrol Boat (2 units)", 750, 485, 'med')

    # Places the user ships
    def userPlace(self):
        delete_buttons()
        user_place_board = [[' ' for x in range(10)] for x in range(10)]
        update, ignore = True, True
        orientation = 'v'
        screen = 0
        for x in self.userShips:
            x_axis, y_axis = 0, 0
            finished = False
            board_copy = copy.deepcopy(user_place_board)
            while not finished:

                # Makes a copy of the board to simply revert changes
                if not ignore and update:
                    deep_copy = copy.deepcopy(board_copy)
                    user_place_board = board_copy
                    board_copy = deep_copy

                # Places the ship on the board
                for y in range(self.userShips[x]):
                    if orientation == 'v':
                        user_place_board[y_axis+y][x_axis] = x
                    else:
                        user_place_board[y_axis][x_axis+y] = x
                # Updates the display
                if update:
                    self.draw_user_place_screen(user_place_board)
                    update = False
                    ignore = False

                # Handles events
                for event in pygame.event.get():

                    # Quits the game and closes the window
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if screen == 0:
                            if event.key == pygame.K_UP:
                                if y_axis != 0:
                                    y_axis -= 1
                                    update = True
                            elif event.key == pygame.K_DOWN:
                                if orientation == 'v':
                                    limit = 10 - self.userShips[x]
                                else:
                                    limit = 9
                                if y_axis != limit:
                                    y_axis += 1
                                    update = True
                            elif event.key == pygame.K_RIGHT:
                                if orientation == 'h':
                                    limit = 10 - self.userShips[x]
                                else:
                                    limit = 9
                                if x_axis != limit:
                                    x_axis += 1
                                    update = True
                            elif event.key == pygame.K_LEFT:
                                if x_axis != 0:
                                    x_axis -= 1
                                    update = True
                            elif event.key == pygame.K_SPACE:
                                if orientation == 'v':
                                    if (x_axis + self.userShips[x]) > 10:
                                        x_axis = (10 - self.userShips[x])
                                    orientation = 'h'
                                else:
                                    if (y_axis + self.userShips[x]) > 10:
                                        y_axis = (10 - self.userShips[x])
                                    orientation = 'v'
                                update = True

                            # Checks the placement of the ship
                            elif event.key == pygame.K_RETURN:
                                finished = self.validatePlacement(False, self.userShips[x], y_axis, x_axis, orientation)
                                update = True
                pygame.display.update()

            # once all ships are placed move the pieces over to the game board
            self.userBoard = user_place_board

        # Tells the main display to start
        global placed
        placed = True

    # Gets all the sunk and to be sunk ships
    def getEnemyFleet(self, computer):
        write_obj = 'Ships to sink:'
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
        write_obj += '['
        for x in sink:
            write_obj += x + ' '
        write_obj += '] Ships sunk:['
        for x in sunk:
            write_obj += x + ' '
        write_obj += ']'
        print(write_obj)

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
            usable_board = self.userBoard
            self.round += 1
        else:
            usable_board = self.computerBoard
        sunk = False

        # Checks if you already made a move there
        if usable_board[x][y] == '*' or usable_board[x][y] == '#':
            messages.insert(0, "Sorry, You've already played there.")
            return usable_board[x][y]
        else:

            # Gets the old symbol in that cell
            old = usable_board[x][y]

            # If a ship was in that cell
            if usable_board[x][y] != ' ':
                usable_board[x][y] = '#'

                # Checks to see if you sunk the ship
                sunk = self.checkIfSunk(computer, old)
                if computer:
                    messages.insert(0, 'The enemy has hit your fleet!!')
                    self.hits[0] += 1
                    if sunk:
                        messages.insert(0, "Your " + self.reference[old][0] + " has been sunk!")
                        self.sunk[0][0] += 1
                        z = 1

                        # Adds the sunk ship to the first empty spot
                        while self.sunk[0][z]:
                            z += 1
                        self.sunk[0][z] = self.reference[old][0]
                else:
                    messages.insert(0, "You've hit the enemy's fleet!!")
                    pygame.mixer.music.load('assets&sounds/Explosion+3.wav')
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play()
                    self.hits[1] += 1
                    if sunk:
                        messages.insert(0, "You've sunk their " + self.reference[old][0])
                        self.sunk[1][0] += 1
                        z = 1

                        # Adds the sunk ship to the first empty spot
                        while self.sunk[1][z]:
                            z += 1
                        self.sunk[1][z] = self.reference[old][0]
            else:
                usable_board[x][y] = '*'
                if computer:
                    self.misses[0] += 1
                    messages.insert(0, 'The enemy has missed your fleet')
                else:
                    self.misses[1] += 1
                    messages.insert(0, "You've missed the enemy fleet")
                    pygame.mixer.music.load('assets&sounds/Water Explosion Sound Effect.wav')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()

            # returns the old cell symbol and if you sunk a ship
            return [old, sunk]

    # Checks to see if a ship was sunk
    def checkIfSunk(self, computer, ship):
        if not computer:
            ships = self.computerShips
        else:
            ships = self.userShips
        ships[ship] -= 1
        return ships[ship] == 0

    # Increments the game rounds
    def incrementRounds(self):
        self.round += 1

    # Checks ahead and behind the current cell to see if there is a limit
    def check_ahead_behind(self, y, x, size):
        limit = [[5, 5], [5, 5]]
        found = [False, False, False, False]
        over = [False, False, False, False]
        for z in range(1, size):

            # Horizontal limit
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

            # Vertical limit
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
    def AI_move(self, coordinates, target):
        global possible_positions
        if diff == 1:
            coordinates = [letters.index(random.choice(letters)), random.randint(0, 9)]
        else:

            # Searches the board for a ship
            if not target:
                possible_positions = []
                if diff == 2:
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
                    available_ships = []
                    for key in self.userShips:
                        if self.userShips[key] != 0:
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
                                #print(y, x, limit, available_ships)
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

                    biggest = []
                    for i in range(2):
                        for y in range(10):
                            for x in range(10):
                                if i == 0:
                                    if possiblelocation[y][x] > largest:
                                        largest = possiblelocation[y][x]
                                else:
                                    if possiblelocation[y][x] == largest:
                                        biggest.append([y, x])
                    '''for x in possiblelocation:
                        print('[', end='')
                        for y in range(10):
                            if x[y] > 9:
                                if y != 9:
                                    print(str(x[y]) + ', ', end='')
                                else:
                                    print(str(x[y]) + ']')
                            else:
                                if y != 9:
                                    print('0' + str(x[y]) + ', ', end='')
                                else:
                                    if x[y] < 10:
                                        print('0' + str(x[y]), end='')
                                    else:
                                        print(str(x[y]), end='')
                                    print(']')
                    print()'''
                    coordinates = random.choice(biggest)
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

                # Pops the last position for the AI to hit
                coordinates = possible_positions.pop()
        return coordinates

    # Saves the game state to .ship file
    def save_game(self):
        try:
            file = open("save_game.ship", "w")
            write_obj = str(self.userShips) + ';' + str(self.computerShips) + ';' + str(self.round) + ';' \
                        + str(self.hits) + ';' + str(self.misses) + ';' + str(diff)
            write_obj += '\n'
            for x in range(2):
                if x == 0:
                    write_board = self.userBoard
                else:
                    write_board = self.computerBoard
                for row in range(10):
                    write_obj += str(write_board[row])
                    if row != 9:
                        write_obj += ','
                write_obj += '\n'
            file.write(write_obj)
            messages.insert(0, 'Game Saved')
            file.close()
        except IOError:
            messages.insert(0, 'Error saving game')

    # Loads the game state from .ship file
    def load_game(self):
        global diff
        try:
            file = open('save_game.ship', 'r')
            x = 0
            for line in file:
                if x == 0:
                    data = line.split(';')
                    self.reset_type(False, True, data[0])
                    self.reset_type(True, True, data[1])
                    self.round = int(data[2])
                    self.reset_type(True, False, data[3])
                    self.reset_type(False, False, data[4])
                    diff = int(data[5])
                else:
                    if x == 1:
                        self.userBoard = ast.literal_eval(line)
                    else:
                        self.computerBoard = ast.literal_eval(line)
                x += 1
            global placed
            placed = True
        except IOError:
            messages.insert(0, 'Failed to load game')

    # Resets the data back to a usable type
    def reset_type(self, computer, dic, data):
        if dic:
            if computer:
                ships = self.computerShips
            else:
                ships = self.userShips
            ships = ast.literal_eval(data)
            for key in ships:
                ships[key] = int(ships[key])
        else:
            data = ast.literal_eval(data)
            for x in range(len(data)):
                data[x] = int(data[x])
            if computer:
                self.hits = data
            else:
                self.misses = data


class Button:
    def __init__(self, msg, x, y, w, h, function, border=0, color=BLACK, size="lrg"):
        self.msg = msg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.function = function
        self.border = border
        self.color = color
        self.size = size

        # appends to current on screen buttons
        self.draw_Button()
        if function != 'None':
            buttons.append(self)

    # draws the button to the screen
    def draw_Button(self):
        pygame.draw.rect(Surface, (115, 115, 115), (self.x, self.y, self.w, self.h), self.border)
        if self.size == 'lrg':
            text_surf = Button_font.render(self.msg, True, self.color)
        else:
            text_surf = text_font.render(self.msg, True, self.color)
        result_rect = text_surf.get_rect()
        result_rect.center = ((self.x + (self.w/2)), (self.y + (self.h/2)))
        Surface.blit(text_surf, result_rect)

    # Checks to see if the button was clicked
    def check_clicked(self):
        if (self.x + self.w) > pygame.mouse.get_pos()[0] > self.x and (self.y + self.h) > pygame.mouse.get_pos()[1] \
                > self.y:
            return True

    # Executes the buttons function
    def execute(self):
        exec(self.function)


def delete_buttons():
    global buttons
    buttons = []


def set_diff(difficulty):
    global diff
    diff = difficulty


# General function for displaying text
def text(msg, x, y, size, color=WHITE):
    if size == 'lrg':
        text_block = title_font.render(msg, True, color)
    elif size == 'med':
        text_block = text_font.render(msg, True, color)
    else:
        text_block = small_font.render(msg, True, color)
    result_rect = text_block.get_rect()
    result_rect = text_block.get_rect()
    result_rect.topleft = (x, y)
    Surface.blit(text_block, result_rect)


# End game screen
def end_game(player):
    delete_buttons()
    Surface.fill((0, 0, 0))
    Surface.blit(background, (0, 0))
    if player:
        text('Congratulations! You have sunk', 150, 155, 'lrg')
        text('the emeny fleet!!', 450, 235, 'lrg')
    else:
        text('The enemy has sunk your fleet!!', 150, 155, 'lrg')
    Button('New Game', (win_width/2) - 150, 315, 300, 50, 'new_game(True)')


# First screen that the user sees
def home_screen():
    global board
    board = BattleshipGame()
    delete_buttons()
    text('Battleship', win_width/2 - 200, 25, 'lrg')
    image = pygame.image.load('assets&sounds/pieces.png')
    Surface.blit(image, ((win_width/2) - 450, 110))
    Button('New Game', (win_width/2) - 150, 375, 300, 50, 'new_game(False)')
    Button('Load Game', (win_width/2) - 150, 450, 300, 50, 'board.load_game()')


# Builds a new game
def new_game(new):

    # Initialize the board and placements of computer ships
    global placed, board
    if new:
        board = BattleshipGame()
    board.comupterPlace()
    placed = False

    delete_buttons()
    Surface.fill((0, 0, 0))
    Surface.blit(background, (0, 0))

    text('Please select a difficulty', win_width/2 - 425, 100, 'lrg')
    Button('Easy', (win_width/2) - 175, 250, 300, 50, 'set_diff(1); board.userPlace()')
    Button('Medium', (win_width/2) - 175, 325, 300, 50, 'set_diff(2); board.userPlace()')
    Button('Hard', (win_width/2) - 175, 400, 300, 50, 'set_diff(3); board.userPlace()')


def main():

    # Initialize GUI settings
    global background, Surface
    pygame.init()
    FPS_clock = pygame.time.Clock()
    Surface = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('Battleship')
    pygame.display.set_icon(pygame.image.load('assets&sounds/Ticonderoga_cruiser.gif'))
    background = pygame.transform.scale(pygame.image.load('assets&sounds/water.png'), (win_width, win_height))
    background.set_alpha(150)
    Surface.blit(background, (0, 0))

    # Font info
    global title_font, Button_font, text_font, small_font
    title_font = pygame.font.Font('freesansbold.ttf', 70)
    Button_font = pygame.font.Font('freesansbold.ttf', 40)
    text_font = pygame.font.Font('freesansbold.ttf', 30)
    small_font = pygame.font.Font('freesansbold.ttf', 15)

    # Display the home screen
    home_screen()

    # messages for user, old content of cell, and whether the users ships have been placed
    global messages, content, placed
    messages = []
    update, target = False, False
    AI_coordinates = [0, -1]
    hits = 0

    while True:
        if not placed:
            player = False
        # Main event loop
        for event in pygame.event.get():
            # Quits the game and closes the window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Checks to see if a button was clicked
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    if button.check_clicked():
                        button.execute()
                        if placed:
                            if board.checkWinning(True):
                                end_game(True)
                            else:
                                player = not player
                                update = True

        # Updates the screen and makes the computers move
        if update:
            if not player:
                content = ['*', None]
                coordinates = board.AI_move(AI_coordinates, target)
                AI_coordinates = coordinates
                content = board.makeA_Move(True, coordinates[0], coordinates[1])
                if diff != 1:
                    if content[0] == ' ':
                        if target:
                            AI_coordinates = recent_hit

                            # If there are no more possible positions to hit from its current cell
                            # goes back to where it first hit
                            if len(possible_positions) == 0:
                                    AI_coordinates = first_hit
                    else:
                        target = True

                        # Saves the first hit
                        if hits == 0:
                            first_hit = coordinates

                        # Saves the most resent hit
                        recent_hit = coordinates

                        # increments the hits
                        hits += 1

                    if content[1]:
                        if hits != board.reference[content[0]][1]:
                            hits -= board.reference[content[0]][1]
                        else:
                            target = False
                            hits = 0
                        # Resets the AI position back to where it first made a hit
                        AI_coordinates = first_hit
                player = not player
            # Checks to see if someone has won
            if board.checkWinning(not player):
                end_game(not player)
            else:
                board.draw_main_screen(False)
            update = False

        # Updates the display
        pygame.display.update()
        FPS_clock.tick(FPS)

if __name__ == '__main__':
    main()
