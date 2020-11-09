import os

class board:

    def __init__(self, xSize, ySize):

        self.xSize = xSize
        self.ySize = ySize

        self.boardObj = make2dList(self.xSize, self.ySize)

        for y in range(0, self.ySize):
            for x in range(0, self.xSize):
                self.set(x, y, piece("none"))

    def printBoard(self):
        for x in self.boardObj:
            line = ""
            for i in x:
                line += i.symbol
            print(line)

    def set(self, xPos, yPos, value):
        self.boardObj[yPos][xPos] = value

    def get(self, xPos, yPos):
        return self.boardObj[yPos][xPos]

def make2dList(rows, cols):
    return [ ([0] * cols) for row in range(rows) ]

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class game:

    def __init__(self, board):

        self.board = board
        self.currentTeam = "white"


    def move(self, xOrg, yOrg, xNew, yNew):
        movingPiece = self.board.get(xOrg, yOrg)
        self.board.set(xOrg, yOrg, piece("none"))
        self.board.set(xNew, yNew, movingPiece)
    

    def placeBlack(self):
        for x in range(0, self.board.xSize):                #Places full row of pawns
            board.set(self.board, x, 1, pawn("black"))
        
        board.set(self.board, 0, 0, rook("black"))
        board.set(self.board, 1, 0, knight("black"))
        board.set(self.board, 2, 0, bishop("black"))
        board.set(self.board, 3, 0, queen("black"))
        board.set(self.board, 4, 0, king("black"))
        board.set(self.board, 5, 0, bishop("black"))
        board.set(self.board, 6, 0, knight("black"))
        board.set(self.board, 7, 0, rook("black"))



    def placeWhite(self):
        for x in range(0, self.board.xSize):                #Places full row of pawns
            board.set(self.board, x, self.board.ySize-2, pawn("white"))

        board.set(self.board, 0, 7, rook("white"))
        board.set(self.board, 1, 7, knight("white"))
        board.set(self.board, 2, 7, bishop("white"))
        board.set(self.board, 3, 7, queen("white"))
        board.set(self.board, 4, 7, king("white"))
        board.set(self.board, 5, 7, bishop("white"))
        board.set(self.board, 6, 7, knight("white"))
        board.set(self.board, 7, 7, rook("white"))
        
    def commandInput(self):
        command = input("option("+self.currentTeam+"): ")
            
        if command == "move":
            posOrg = input("original position(example: 0,1): ")
            posNew = input("new position(example: 0,3): ")

            if ',' not in posOrg or ',' not in posNew:
                print("Invalid syntax.")
                input()
                return

            oldPos = posOrg.split(',')
            newPos = posNew.split(',')

            if self.board.get(int(oldPos[0]), int(oldPos[1])).team != self.currentTeam:
                print("WRONG TEAM SUCKA")
                input()
                return
                
            try:
                self.move(int(oldPos[0]), int(oldPos[1]), int(newPos[0]), int(newPos[1]))
            except IndexError:
                print("Value is larger than the board.")
                input()
            except ValueError:
                print("Invalid syntax.")
                input()
                

        if command == "help":
            print("move, moves a piece.\nstop, exits the program")
            input()

        if command == "stop":
            self.playing = False


    def whiteTurn(self):
        cls()
        self.currentTeam = "white"
        self.board.printBoard()
        self.commandInput()
        
    def blackTurn(self):
        cls()
        self.currentTeam = "black"
        self.board.printBoard()
        self.commandInput()


    def startGame(self):

        self.playing = True
        self.placeBlack()
        self.placeWhite()

        while self.playing:
            if self.playing:
                self.whiteTurn()
            if self.playing:
                self.blackTurn()

            
    

class piece:

    symbol = '0'
    def __init__(self, team):
        if team == "black" or team == "white" or team == "none":
            self.team = team
        else:
            print(team + " is not a valid team.")

    def isTeam(self, teamName):
        return self.team == teamName

class king(piece):
    symbol = 'K'

class queen(piece):
    symbol = 'Q'

class rook(piece):
    symbol = 'R'

class bishop(piece):
    symbol = 'B'

class knight(piece):
    symbol = 'N'

class pawn(piece):
    symbol = 'P'

def main():
    b = board(8, 8)
    g = game(b)
    g.startGame()

if __name__ == "__main__":
    main()




#to-do: def whiteTurn at start of game after placing teams. move current inputs to another def, do move method, if piece at first position isTeam("white") do move as usual
#if !isTeam("white") print("Invalid piece"), at end of def whiteTurn return and then next in startgame is def blackTurn which does the same except with black team.
#
#       def startgame:
#           self.playing = True
#           self.placeBlack()
#           self.placeWhite()
#           while self.playing:
#               self.whiteTurn()
#               self.blackTurn()
#               self.board.printBoard()
#
#
#
#to-do: change commandInput method to only have start and stop commands and make movementInput method which just does the movement and can do stop as well, call commandInput once before self.playing is set to true
#at the start of whiteTurn and blackTurn use movementInput call instead of commandInput to bypass initial menu.