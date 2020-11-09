class board:

    def __init__(self, xSize, ySize):

        self.xSize = xSize
        self.ySize = ySize

        self.boardObj = make2dList(self.xSize, self.ySize)

    def printBoard(self):
        for x in self.boardObj:
            print(x)

    def set(self, xPos, yPos, value):
        self.boardObj[yPos][xPos] = value

    def get(self, xPos, yPos):
        return self.boardObj[yPos][xPos]

def make2dList(rows, cols):
    return [ ([0] * cols) for row in range(rows) ]

class game:

    def __init__(self, board):

        self.board = board


    def move(self, xOrg, yOrg, xNew, yNew):
        piece = self.board.get(xOrg, yOrg)
        self.board.set(xOrg, yOrg, 0)
        self.board.set(xNew, yNew, piece)
    

    def placeBlack(self):
        for y in range(0, 2):
            for x in range(0, self.board.xSize):
                board.set(self.board, x, y, 1)
    def placeWhite(self):
        for y in range(self.board.ySize-2, self.board.ySize):
            for x in range(0, self.board.xSize):
                board.set(self.board, x, y, 1)


    def startGame(self):

        self.playing = True
        self.placeBlack()
        self.placeWhite()

        while self.playing:
            self.board.printBoard()

            command = input("option(help): ")

            if command == "move":
                posOrg = input("original position(example: 0,1): ")
                posNew = input("new position(example: 0,3): ")

                if ',' not in posOrg or ',' not in posNew:
                    print("Invalid syntax.")
                    continue

                oldPos = posOrg.split(',')
                newPos = posNew.split(',')
                
                try:
                    self.move(int(oldPos[0]), int(oldPos[1]), int(newPos[0]), int(newPos[1]))
                except IndexError:
                    print("Value is larger than the board.")
                except ValueError:
                    print("Invalid syntax.")

            if command == "help":
                print("move, moves a piece.\nstop, exits the program")

            if command == "stop":
                self.playing = False
    
        

def main():
    b = board(8, 8)
    g = game(b)
    g.startGame()

if __name__ == "__main__":
    main()
