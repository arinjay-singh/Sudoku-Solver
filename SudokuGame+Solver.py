#This is my own work, signed Arinjay Singh, date: June 1, 2020
#Introduction to Computer Science
#Final Project
##################
#Sudoku
##################

#import objects from tkinter module
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

#create Sudoku board using 2D list
sudokuBoard = [
    [0,9,0,0,0,4,0,0,5],
    [0,0,7,8,2,0,0,1,0],
    [0,3,0,1,0,0,2,0,0],
    [0,0,0,0,0,0,0,7,2],
    [8,1,0,0,3,0,0,0,0],
    [0,4,0,0,6,0,0,0,0],
    [0,0,0,0,1,0,9,2,0],
    [0,0,0,0,0,0,0,0,0],
    [6,0,0,0,5,0,0,0,0]
    ]
#solved version of Sudoku Board
solvedBoard = [
    [2,9,1,6,7,4,8,3,5],
    [5,6,7,8,2,3,4,1,9],
    [4,3,8,1,9,5,2,6,7],
    [9,5,6,4,8,1,3,7,2],
    [8,1,2,9,3,7,5,4,6],
    [7,4,3,5,6,2,1,9,8],
    [3,8,5,7,1,6,9,2,4],
    [1,7,9,2,4,8,6,5,3],
    [6,2,4,3,5,9,7,8,1]
    ]

#set dimensions of Sudoku board
cellWidth = 50
windowMargin = 20
windowWidth = windowMargin * 2 + cellWidth * 9
windowHeight = windowWidth

#create Sudoku GUI class that inherits from Frame from tkinter
class SudokuGUI(Frame):
    #initial method that takes 2 arguments, the tkinter window and an instance of the Game Logic class
    def __init__(self, window, game):
        #set class attributes
        self.game = game
        self.window = window
        #call initial method of Frame tkinter class
        Frame.__init__(self, window)
        self.row = 0
        self.column = 0
        #call method to create interface
        self.createInterface()

    #create interface for game
    def createInterface(self):
        #create title of window
        self.window.title("Sudoku")
        self.pack(fill = BOTH, expand = 1)
        #create canvas
        self.canvas = Canvas(self,width = windowWidth,height = windowHeight)
        self.canvas.pack(fill = BOTH,side = TOP)
        #create buttons to close, clear and solve
        closeButton = Button(self,text = "Close",command = self.window.destroy)
        closeButton.pack(fill = BOTH,side = BOTTOM)
        clearButton = Button(self,text = "Clear",command = self.clearBoard)
        clearButton.pack(fill = BOTH,side = BOTTOM)
        solveButton = Button(self,text = "Solve",command = self.solveBoard)
        solveButton.pack(fill = BOTH,side = BOTTOM)
        #call drawBoard method
        self.drawBoard()
        #call drawNumbers method
        self.drawNumbers()
        #assign keyboard events to methods
        self.canvas.bind("<Button-1>", self.squareClicked)
        self.canvas.bind("<Key>", self.takeNumberInput)

    #create Sudoku board
    def drawBoard(self):
        for x in range(10):
            #set different line widths to make 3x3 subsections clearer
            if x % 3 == 0:
                lineWidth = 4
            else:
                lineWidth = 1
            #draw the vertical lines of grid
            xPos1 = windowMargin + x * cellWidth
            yPos1 = windowMargin
            xPos2 = windowMargin + x * cellWidth
            yPos2 = windowHeight - windowMargin
            self.canvas.create_line(xPos1,yPos1,xPos2,yPos2,fill = "black",width = lineWidth)
            #draw the horizontal lines of grid
            xPos1 = windowMargin
            yPos1 = windowMargin + x * cellWidth
            xPos2 = windowWidth - windowMargin
            yPos2 = windowMargin + x * cellWidth
            self.canvas.create_line(xPos1,yPos1,xPos2,yPos2,fill = "black",width = lineWidth)

    #draw numbers into Sudoku board
    def drawNumbers(self):
        #for each square in the board
        for row in range(9):
            for column in range(9):
                num = self.game.puzzle[row][column]
                #if the square is not empty
                if num != 0:
                    #if the number is part of the original board
                    if num == self.game.startingPuzzle[row][column]:
                        #set font color to black
                        color = "black"
                    #otherwise if number inputed by user
                    else:
                        #set font color to blue
                        color = "blue"
                    #find coordinates of square
                    x = windowMargin + column * cellWidth + cellWidth / 2
                    y = windowMargin + row * cellWidth + cellWidth / 2
                    #draw the number in its corresponding square
                    self.canvas.create_text(x,y,text = num,tag = "numbers",fill = color)

    #clear board when "Clear" button is clicked
    def clearBoard(self):
        #call start game method using GameLogic object
        self.game.startGame()
        #delete victory screen
        self.canvas.delete("victory")
        #delete previous numbers
        self.canvas.delete("numbers")
        #call drawNumbers method to update Sudoku board
        self.drawNumbers()

    #solve board when "Solve" button is clicked
    def solveBoard(self):
        #clear the sudoku board
        self.clearBoard()
        #draw complete solution into board 
        #for each square in the board
        for row in range(9):
            for column in range(9):
                num = solvedBoard[row][column]
                #find coordinates of square
                x = windowMargin + column * cellWidth + cellWidth / 2
                y = windowMargin + row * cellWidth + cellWidth / 2
                #draw the number in its corresponding square
                self.canvas.create_text(x,y,text = num,tag = "numbers",fill = "black")

    #find which square was clicked
    def squareClicked(self,event):
        #if game is over, don't do anything
        if self.game.gameOver:
            return
        #get event coordinates
        x = event.x
        y = event.y
        #if x-coordinate is on board
        if windowMargin < x < windowWidth - windowMargin:
            #if y-coordinate is on board
            if windowMargin < y < windowHeight - windowMargin:
                #set focus of keyboard events to canvas
                self.canvas.focus_set()
                #find row and column location 
                row = int((y - windowMargin)/cellWidth)
                column = int((x - windowMargin)/cellWidth)
                #set class attributes to location of click if not already clicked
                if row == self.row and column == self.column:
                    self.row = -1
                    self.column = -1
                elif self.game.puzzle[row][column] == 0:
                    self.row = row
                    self.column = column
        #call method to highlight the square that has been clicked
        self.highlightSquare()

    #outline the square that has been clicked with blue box
    def highlightSquare(self):
        #delete previous highlighted box
        self.canvas.delete("highlight")
        #if not already clicked
        if self.row >= 0 and self.column >= 0:
            #find x and y positions of top left corner and bottom right corner of square
            xPos1 = windowMargin + self.column * cellWidth + 1
            yPos1 = windowMargin + self.row * cellWidth + 1
            xPos2 = windowMargin + (self.column + 1) * cellWidth - 1
            yPos2 = windowMargin + (self.row + 1) * cellWidth - 1
            #create blue box around square
            self.canvas.create_rectangle(xPos1,yPos1,xPos2,yPos2,outline = "blue",tag = "highlight")

    #take number input from user
    def takeNumberInput(self,event):
        #if game is over return nothing
        if self.game.gameOver:
            return
        valid = "1234567890"
        #if not already clicked
        if self.row >= 0 and self.column >= 0:
            #if number is valid
            if event.char in valid:
                #set the square to the user's input
                self.game.puzzle[self.row][self.column] = int(event.char)
                #set location back to (-1,-1)
                self.row = -1
                self.column = -1
                #call drawNumbers to update board
                self.drawNumbers()
                #call highlightSquare to remove highlight from square
                self.highlightSquare()
                #if game is is over, draw the winning screen
                if game.checkIfCompleted():
                    self.drawVictoryScreen()

    #draw winning screen
    def drawVictoryScreen(self):
        #find x and y positions for oval
        xPos1 = windowMargin + cellWidth * 3
        yPos1 = windowMargin + cellWidth * 3
        xPos2 = windowMargin + cellWidth * 6
        yPos2 = windowMargin + cellWidth * 6
        #draw oval in middle of screen
        self.canvas.create_oval(xPos1,yPos1,xPos2,yPos2,fill = "green",tag = "victory")
        #find x and y positions for text
        x = windowMargin + 4 * cellWidth + cellWidth / 2
        y = windowMargin + 4 * cellWidth + cellWidth / 2
        #draw winning message inside the oval
        self.canvas.create_text(x,y,text = "YOU WIN",tag = "victory",fill = "white",font = ("Arial",22))
    
#create Game Logic class
class GameLogic:
    #initial method with 1 argument, the board
    def __init__(self, board):
        #set class attributes
        self.startingPuzzle = board
        self.gameOver = False
        
    #method to setup game to be started
    def startGame(self):
        #set game over to false
        self.gameOver = False
        #create copy of starting puzzle
        self.puzzle = []
        for row in range(9):
            self.puzzle.append([])
            for col in range(9):
                self.puzzle[row].append(self.startingPuzzle[row][col])
                
    #check if player has completed the Sudoku board
    def checkIfCompleted(self):
        #check all rows
        for row in range(9):
            if not self.checkRow(row):
                return False
        #check all columns
        for column in range(9):
            if not self.checkColumn(column):
                return False
        #check all 3x3 boxes
        for row in range(3):
            for column in range(3):
                if not self.checkBox(row, column):
                    return False
        #if all true, set gameOver to true 
        self.gameOver = True
        #return true
        return True

    #check list for numbers 1-9
    def checkNumbers(self,lst):
        return set(lst) == set(range(1,10))

    #check if row is valid
    def checkRow(self,row):
        #return boolean value
        return self.checkNumbers(self.puzzle[row])

    #check if column is valid
    def checkColumn(self,column):
        columnItems = []
        for row in range(9):
            columnItems.append(self.puzzle[row][column])
        #return boolean value
        return self.checkNumbers(columnItems)

    #check if 3x3 box is valid
    def checkBox(self,row,column):
        boxItems = []
        boxPosX = column//3
        boxPosY = row//3
        for r in self.puzzle:
            for c in r:
                if r.index(c)//3 == boxPosX and self.puzzle.index(r)//3 == boxPosY:
                    boxItems.append(self.puzzle[self.puzzle.index(r)][r.index(c)])
        #return boolean value
        return self.checkNumbers(boxItems)
    
#run game
if __name__ == '__main__':
    #create instance of game logic class
    game = GameLogic(sudokuBoard)
    #call start game method
    game.startGame()
    #create window
    window = Tk()
    #create instance of Sudoku GUI class
    SudokuGUI(window,game)
    #use mainloop to run game
    window.mainloop()
