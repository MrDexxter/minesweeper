import tkinter, tkinter.simpledialog, tkinter.messagebox, configparser, os
from random import randint
from functools import total_ordering

@total_ordering
class GameBoard:
    'This class will make GameBoards. A Game Board is reffered to as an environment to play our game. It will have grid accompanied by a Menu Bar'

    gameboard = tkinter.Tk()
    gameboard.title("MINESWEEPER")
    colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']

    def __init__(self, columns = 10, rows = 10, mines= 10, Game_Over = False):
        self.columns = columns
        self.rows = rows
        self.mines = mines
        self.Game_Over = Game_Over
        self.field = []
        self.all_buttons = []

    def click_button(self, x, y):
        '''This defines the function of clicking on any button in Grid. Clicking a button will display
        the number of mines that are surrounding that button. If there is no mine than it will call the Auto-Click Button
        that will display the '''
        self.all_buttons[x][y]["text"] = str(self.field[x][y])
        if self.field[x][y] == -1:
            self.all_buttons[x][y]["text"] = "*"
            self.all_buttons[x][y].config(background='red', disabledforeground='black')
            self.Game_Over= True
            tkinter.messagebox.showinfo("Game Over", "You have lost.")
            # now show all other mines
            for _x in range(0, self.rows):
                for _y in range(self.columns):
                    if self.field[_x][_y] == -1:
                        self.all_buttons[_x][_y]["text"] = "*"
        else:
            self.all_buttons[x][y].config(disabledforeground=self.colors[self.field[x][y]])
        if self.field[x][y] == 0:
            self.all_buttons[x][y]["text"] = " "
            # now repeat for all buttons nearby which are 0... kek
            self.AutoClick(x, y)
        self.all_buttons[x][y]['state'] = 'disabled'
        self.all_buttons[x][y].config(relief=tkinter.SUNKEN)
        self.checkWin()


    def checkWin(self):
        'It is necessary to check the winning statistic after every move. For that purpose, this function will cehck and displays the win if user has won the game.'
        win = True
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                if self.field[x][y] != -1 and self.all_buttons[x][y]["state"] == "normal":
                    win = False
        if win:
            tkinter.messagebox.showinfo("Gave Over", "You have won.")

    def AutoClick(self, x, y):
        if self.all_buttons[x][y]["state"] == "disabled":
            return
        if self.field[x][y] != 0:
            self.all_buttons[x][y]["text"] = str(self.field[x][y])
        else:
            self.all_buttons[x][y]["text"] = " "
        self.all_buttons[x][y].config(disabledforeground=self.colors[self.field[x][y]])
        self.all_buttons[x][y].config(relief=tkinter.SUNKEN)
        self.all_buttons[x][y]['state'] = 'disabled'
        if self.field[x][y] == 0:
            if x != 0 and y != 0:
                self.AutoClick(x - 1, y - 1)
            if x != 0:
                self.AutoClick(x - 1, y)
            if x != 0 and y != self.columns - 1:
                self.AutoClick(x - 1, y + 1)
            if y != 0:
                self.AutoClick(x, y - 1)
            if y != self.columns - 1:
                self.AutoClick(x, y + 1)
            if x != self.rows - 1 and y != 0:
                self.AutoClick(x + 1, y - 1)
            if x != self.rows - 1:
                self.AutoClick(x + 1, y)
            if x != self.rows - 1 and y != self.columns - 1:
                self.AutoClick(x + 1, y + 1)

    def Right_Click(self, abscissa, ordinate):
        '''User can also mark some tiles for which he cannot predict wether they are mines or not.
            This function if used to do so and displays a question mark over the marked tile. '''
        if self.Game_Over:
            return
        if self.all_buttons[abscissa][ordinate]["text"] == "?":
            self.all_buttons[abscissa][ordinate]["text"] = " "
            self.all_buttons[abscissa][ordinate]["state"] = "normal"
        elif self.all_buttons[abscissa][ordinate]["text"] == " " and self.all_buttons[abscissa][ordinate]["state"] == "normal":
            self.all_buttons[abscissa][ordinate]["text"] = "?"
            self.all_buttons[abscissa][ordinate]["state"] = "disabled"

    def prepare_game(self):
        'It will prepare the game i.e. randomly assign mines to some tiles and assign numbers to remaining tiles based on the position of mines'
        self.field = []
        for i in range(0, self.rows):
            self.field.append([])
            for j in range(0, self.columns):
                self.field[i].append(0)
        # Generate Mines
        for _ in range(self.mines):
            x_axis = randint(0, self.rows - 1)
            y_axis = randint(0, self.columns - 1)
            # prevent duplicate mines at one place
            while self.field[x_axis][y_axis] == -1:
                x_axis = randint(0, self.rows - 1)
                y_axis = randint(0, self.columns - 1)
            self.field[x_axis][y_axis] = -1
            if x_axis != 0:
                if y_axis != 0:
                    if self.field[x_axis - 1][y_axis - 1] != -1:
                        self.field[x_axis - 1][y_axis - 1] = int(self.field[x_axis - 1][y_axis - 1]) + 1
                if self.field[x_axis - 1][y_axis] != -1:
                    self.field[x_axis - 1][y_axis] = int(self.field[x_axis - 1][y_axis]) + 1
                if y_axis != self.columns - 1:
                    if self.field[x_axis - 1][y_axis + 1] != -1:
                        self.field[x_axis - 1][y_axis + 1] = int(self.field[x_axis - 1][y_axis + 1]) + 1
            if y_axis != 0:
                if self.field[x_axis][y_axis - 1] != -1:
                    self.field[x_axis][y_axis - 1] = int(self.field[x_axis][y_axis - 1]) + 1
            if y_axis != self.columns - 1:
                if self.field[x_axis][y_axis + 1] != -1:
                    self.field[x_axis][y_axis + 1] = int(self.field[x_axis][y_axis + 1]) + 1
            if x_axis != self.rows - 1:
                if y_axis != 0:
                    if self.field[x_axis + 1][y_axis - 1] != -1:
                        self.field[x_axis + 1][y_axis - 1] = int(self.field[x_axis + 1][y_axis - 1]) + 1
                if self.field[x_axis + 1][y_axis] != -1:
                    self.field[x_axis + 1][y_axis] = int(self.field[x_axis + 1][y_axis]) + 1
                if y_axis != self.columns - 1:
                    if self.field[x_axis + 1][y_axis + 1] != -1:
                        self.field[x_axis + 1][y_axis + 1] = int(self.field[x_axis + 1][y_axis + 1]) + 1

    def make_gameboard(self):
        'It will make the gameboard in the form of buttons and displays them on the screen.'
        restarter = tkinter.Button(self.gameboard, text="Restart The Game!", command=self.restart_game)
        restarter.grid(row=0, column=0, columnspan=self.columns,sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        self.all_buttons = []
        for x in range(0, self.rows):
            self.all_buttons.append([])
            for y in range(0, self.columns):
                b = tkinter.Button(self.gameboard, text=" ", width=3, command=lambda x=x, y=y: self.click_button(x, y))
                b.bind("<Button-3>", lambda e, x=x, y=y: self.Right_Click(x, y))
                b.grid(row=x + 1, column=y, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
                self.all_buttons[x].append(b)

    def loadConfig(self):
        'This function is used to load the previously saved configuartion for the game.'
        config = configparser.ConfigParser()
        config.read("configurations.ini")
        self.rows = config.getint("Game Attributes", "rows")
        self.cols = config.getint("Game Attributes", "columns")
        self.mines = config.getint("Game Attributes", "mines")

    def save_gameboard_configuration(self):
        'This function will save current configuration in a config file created using configparser'
        configurations = configparser.ConfigParser()
        configurations.add_section("Game Attributes")
        configurations.set("Game Attributes", "rows", str(self.rows))
        configurations.set("Game Attributes", "columns", str(self.columns))
        configurations.set("Game Attributes", "mines", str( self.mines))
        with open("configurations.ini", "w") as file:
            configurations.write(file)


    def MenuBar(self):
        'It is used to create the menu bar'
        menubar = tkinter.Menu(self.gameboard)
        menubar_commands = tkinter.Menu(self.gameboard, tearoff=0)
        menubar_commands.add_command(label="Rookie: (10 x 10 board with 10 mines)",
                                     command=lambda: self.makegrid(10, 10, 10))
        menubar_commands.add_command(label="Soldier: (15 x 15 board with 25 mines)",
                                     command=lambda: self.makegrid(15, 15, 25))
        menubar_commands.add_command(label="Veteran: (25 x 25 board with 50 mines)",
                                     command=lambda: self.makegrid(25, 25, 50))
        menubar_commands.add_command(label="Customize Your Game", command=self.custom_size)
        menubar.add_cascade(label="SIZE", menu=menubar_commands)
        menubar.add_command(label="EXIT", command=self.gameboard.destroy)
        self.gameboard.config(menu=menubar)


    def makegrid(self, row, column, mine):
        'It will initiate the current grid. It will first save the game board conguration for the current game and then call the restart_game function to initiate the grid.'
        self.rows, self.columns, self.mines = row, column, mine
        self.save_gameboard_configuration()
#       self.restart_game()

    def custom_size( self):
        "This is to set the customizeable size"
        self.rows = tkinter.simpledialog.askinteger("Custom Size", "Enter Number Of Rows You Want")
        self.columns = tkinter.simpledialog.askinteger("Custom Size", "Enter Number Of Columns You Want")
        self.mines = tkinter.simpledialog.askinteger("Custom Size", "Enter Number Of Mines You want: ")
        while self.mines > self.rows * self.columns:
            self.mines = tkinter.simpledialog.askinteger("Custom Size",f"Maxiumum Number of Mines should be less than {self.rows * self.columns}")
        self.makegrid(self.rows, self.columns, self.mines)
        self.MenuBar()

    def __lt__(self, other):
        'Tells if one GameBoard is smaller than other based on the area'
        return (self.columns*self.rows < other.columns*other.rows)

    def __eq__(self, other):
        'Returns True if area of one GameBoard is equal to the other'
        return (self.columns*self.rows == other.columns*other.rows)

    def __abs__(self):
        return (self.columns*self.rows)

class MineSweeper(GameBoard):
    "This is a class inherited from the GameBoard Class. It will use that GameBoard to play the minesweeper game."

    def start_game(self):
        'It will create a gaming environment to playt minesweeper using different functions.'
        if os.path.exists("configurations.ini"):
            self.loadConfig()
        else:
            self.save_gameboard_configuration()
        self.MenuBar()
        self.make_gameboard()
        self.prepare_game()
        self.gameboard.mainloop()

    def statistics(self):
        'This function is used to show the statistices of the game'
        if os.path.exists("statistics.ini"):
            Games_Played, Games_Won = self.previous_statistics()
            if not(Games_Won):
                Games_Won += 1
            Games_Played +=1
            statistics_window = tkinter.Tk()
            msg = tkinter.Message(statistics_window, text = f"Games Played = {Games_Played} Games Won = {Games_Won}")
            msg.pack()
            self.save_statitistics(Games_Played, Games_Won)
        else:
            Games_Played, Games_Won = 1, 0
            if self.Game_Over:
                Games_Won = 1
            statistics_window = tkinter.Tk()
            tkinter.Message(statistics_window, text = "Games Played = f{Games_Played} Games Won = f{Games_Won}")
            self.save_statitistics(Games_Played, Games_Won)

    def previous_statistics(self):
        'This function is used to load the previously saved configuartion for the game.'
        config = configparser.ConfigParser()
        config.read("statistics.ini")
        Games_Played = config.getint("Game Statistics", "All Games")
#        Win_Percentage = config.getint("Game Statistics", "Win Percentage")
        Games_Won = config.getint("Game Statistics", "Games Won")
        return (Games_Played, Games_Won)

    @staticmethod
    def save_statitistics(Games_Played, Games_Won):
        'This function will save current configuration in a config file created using configparser'
        configurations = configparser.ConfigParser()
        configurations.add_section("Game Statistics")
        configurations.set("Game Statistics", "All Games", str(Games_Played))
 #       configurations.set("Game Statistics", "Win Percentage", str((Games_Won/Games_Played)*100))
        configurations.set("Game Statistics", "Games Won", str( Games_Won))
        with open("statistics.ini", "w") as file:
            configurations.write(file)

    def restart_game(self):
        'Restart the game after every Turn'
        self.statistics()
        'Delete previous widget and make a new one'
        self.Game_Over = False
        for x in self.gameboard.winfo_children():
            if type(x) != tkinter.Menu:
                x.destroy()
        self.make_gameboard()
        self.prepare_game()

MS = MineSweeper()
MS.start_game()