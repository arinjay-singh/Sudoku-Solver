#Arinjay Singh
#Sudoku Solver 2.0
#May 6, 2020
###############
#This algorithm uses recursion to solve any 9x9 Sudoku puzzle
###############

#import turtle module
import turtle
#import sys module 
import sys

#create Sudoku board
board = [
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

#draw sudoku board using turtle
def drawBoard(t):
    turtle.tracer(0)
    t.shape("blank")
    xPos = -250
    yPos = -250
    t.left(90)
    for x in range(10):
        t.up()
        t.goto(xPos,yPos)
        t.down()
        if x % 3 == 0:
            t.pensize(5)
        else:
            t.pensize(1)
        t.forward(450)
        if x < 9:
            xPos += 50
    t.left(90)
    for x in range(10):
        t.up()
        t.goto(xPos,yPos)
        t.down()
        if x % 3 == 0:
            t.pensize(5)
        else:
            t.pensize(1)
        t.forward(450)
        if x < 9:
            yPos += 50
    turtle.update()
    
#find position of box
def findPos(x,y):
    #find x coordinate
    xPos = -225 + (50*x)
    #find y coordinate
    yPos = 175 - (50*y)
    return [xPos,yPos]

#update board's numbers
def updateBoard(t, board):
    t.shape("blank")
    t.speed(0)
    t.up()
    for row in board:
        for num in row:
            xPos = row.index(num)
            yPos = board.index(row)
            pos = findPos(xPos,yPos)
            t.goto(pos[0]-5,pos[1]-10)
            if num != 0:
                t.write(num, font = ("Arial",15,"normal"))

#check if number is a valid solution
def valid(board,x,y,num):
    #row
    row = board[y]

    #column
    column = []
    for i in range(9):
        column.append(board[i][x])
    #box
    box = []
    boxPosX = x//3
    boxPosY = y//3
    for b in board:
        for a in b:
            if b.index(a)//3 == boxPosX and board.index(b)//3 == boxPosY:
                box.append(board[board.index(b)][b.index(a)])
    #check that the same number isn't in row, column, or box
    if num not in row and num not in column and num not in box:
        return True
    else:
        return False

#solve board using recursion
def solve(t, board):
    for x in range(9):
        for y in range(9):
            if board[y][x] == 0:
                for num in range(1,10):
                    if valid(board,x,y,num):
                        board[y][x] = num
                        solve(t, board)
                        board[y][x] = 0
                return None
    turtle.tracer(1)
    updateBoard(t,board)
    sys.exit()
    
#draw sudoku board
win = turtle.Screen()
sudokuBoard = turtle.Turtle()
drawBoard(sudokuBoard)
numbers = turtle.Turtle()
updateBoard(numbers,board)

#solve sudoku board
solve(numbers,board)
