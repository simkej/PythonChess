'''P-uppgift, spelar schack'''
import sys

class board: #Class för att skapa spelbrädet

    def __init__(self, xSize, ySize):

        self.xSize = xSize
        self.ySize = ySize

        self.boardObj = make2dList(self.xSize, self.ySize)

        for y in range(0, self.ySize):
            for x in range(0, self.xSize):
                self.set(x, y, piece("none"))

    def printBoard(self): #Skriver ut brädet
        for x in self.boardObj:
            line = ""      
            for i in x:
                line += i.symbol
            print(line)

    def printLegalMoves(self, moves):
        #print(moves)
        ursprBoard = []
        for x in moves:
            if self.get(int(x[0]),int(x[1])).symbol != 'X':
                ursprBoard.append([int(x[0]),int(x[1]),self.get(int(x[0]),int(x[1])).symbol])
               # print(ursprBoard)
                self.get(int(x[0]),int(x[1])).symbol = 'X'
        self.printBoard()
        #print(ursprBoard)
        for x in ursprBoard:
            self.get(int(x[0]),int(x[1])).symbol = x[2]
         #   print("bye")
            

    def get(self, xPos, yPos): #Hämtar nuvarande position i lista
        try:
            return self.boardObj[yPos][xPos]
        except IndexError:
            return #Fixa error-meddelande

    def set(self, xPos, yPos, value): #Placerar ut ny position
        self.boardObj[yPos][xPos] = value

class game:

    def __init__(self, board):

        self.board = board
        self.currentTeam = "vit"
    
    def move(self, xOrg, yOrg, xNew, yNew): #Förflyttar pjäs, mha get och set.
        legalmove = self.legalmove(xOrg, yOrg)
        wantedmove = [xNew, yNew]
        if wantedmove in legalmove:
            movingPiece = self.board.get(xOrg, yOrg)            
            self.board.set(xOrg, yOrg, piece("none"))
            self.board.set(xNew, yNew, movingPiece)
        else:
            print("Ej lagligt drag")
            self.commandInput()

    def legalmove(self, xOrg, yOrg):                        #Bestämmer lagliga moves för pieces
        piece = self.board.get(xOrg, yOrg)
        moves = []
        for i in piece.movements:
            if self.board.get(xOrg+i[0],yOrg+i[1]) is not None and int(xOrg+i[0])>-1 and int(yOrg+i[1])>-1 :
         #       print(i)
                if self.board.get(xOrg+i[0],yOrg+i[1]).team == "none":
                    moves.append([xOrg+i[0],yOrg+i[1]])
               #     print(moves)
        return moves

    def placeSvart(self):
        for x in range(0, self.board.xSize):                #Placerar ut raden med svarta bönder
            board.set(self.board, x, 1, pawn("svart"))
        
        board.set(self.board, 0, 0, rook("svart"))          #Placerar resterande svarta pjäser
        board.set(self.board, 1, 0, knight("svart"))
        board.set(self.board, 2, 0, bishop("svart"))
        board.set(self.board, 3, 0, queen("svart"))
        board.set(self.board, 4, 0, king("svart"))
        board.set(self.board, 5, 0, bishop("svart"))
        board.set(self.board, 6, 0, knight("svart"))
        board.set(self.board, 7, 0, rook("svart"))
                
    def placeVit(self):
        for x in range(0, self.board.xSize):                #Placerar ut raden med vita bönder
            board.set(self.board, x, self.board.ySize-2, pawn("vit"))

        board.set(self.board, 0, 7, rook("vit"))          #Placerar resterande vita pjäser
        board.set(self.board, 1, 7, knight("vit"))
        board.set(self.board, 2, 7, bishop("vit"))
        #print(self.board.get(2,7))
        board.set(self.board, 3, 7, queen("vit"))
        board.set(self.board, 4, 7, king("vit"))
        board.set(self.board, 5, 7, bishop("vit"))
        board.set(self.board, 6, 7, knight("vit"))
        board.set(self.board, 7, 7, rook("vit"))

    def commandInput(self): #Tar inputs om förflyttningar. 
        command = input("Vad vill "+self.currentTeam+" göra?(move, help eller stop): ")
            
        if command == "move":
            posOrg = input("Position av pjäs du vill flytta: ")
            oldPos = posOrg.split(',')

            if ',' not in posOrg:
                print("Ogiltigt val.")
                self.commandInput()

            #if len(oldPos) > 8:
             #   print("Ogiltigt val.")
               # self.commandInput()

            self.board.printLegalMoves(self.legalmove(int(oldPos[0]),int(oldPos[1])))
            posNew = input("Positionen du vill flytta den till: ")

            if ',' not in posNew:
                print("Ogiltigt val.")
                self.commandInput()

            newPos = posNew.split(',')

            if self.board.get(int(oldPos[0]), int(oldPos[1])).team != self.currentTeam:
                print("Inte din pjäs att flytta.")
                self.commandInput()
                
            try:
                self.move(int(oldPos[0]), int(oldPos[1]), int(newPos[0]), int(newPos[1]))
            except IndexError:
                print("Värdet är utanför brädet.")
                self.commandInput()
            except ValueError:
                print("Ogiltigt val.")
                self.commandInput()
                

        if command == "help":
            print("'move', anger vilken pjäs du vill flytta och vart. \nförsta koordinaten anger kolonn och andra rad, räkning från 0 till 7. \nExempelvis väljs bonden framför vits kung genom [4,6]  \n'stop', avslutar programmet")
            self.commandInput()

        if command == "stop":
            self.playing = False

    def VitTurn(self): #Kontrollerar om det är vits tur att spela
        self.currentTeam = "vit"
        self.board.printBoard()
        self.commandInput()
        
    def SvartTurn(self): #Kontrollerar om det är svarts tur att spela
        self.currentTeam = "svart"
        self.board.printBoard()
        self.commandInput()


    def startGame(self): #Startar spelet
        self.playing = True
        self.placeSvart()
        self.placeVit()

        while self.playing:
            if self.playing:
                self.VitTurn()
            if self.playing:
                self.SvartTurn()

class piece: #Kontrollerar färg, samt hjälper att rensa efter flyttning.
    symbol = '0'
    def __init__(self, team):
        if team == "svart" or team == "vit" or team == "none":
            self.team = team
        else:
            print(team + " is not a valid team.")

class king(piece): #Klass för kungen med möjliga drag
    symbol = 'K'
    movements = []
    for x in range(-1,2):
        movements.append([0,x])
        movements.append([x,0])
        movements.append([x,x])
        movements.append([x,-x])
        movements.append([-x,x])
        movements.append([-x,-x])
        
class queen(piece): #Klass för damen med möjliga drag
    symbol = 'Q'
    movements = []
    for x in range(-8,8):
        movements.append([0,x])
        movements.append([x,0])
        movements.append([x,x])
        movements.append([x,-x])
        movements.append([-x,x])
        movements.append([-x,-x])

class rook(piece): #Klass för tornet med möjliga drag
    symbol = 'R'
    movements = []
    for x in range(-8,8):    #fundera om förbättring, för att bli mer scaleable
        movements.append([0,x])
        movements.append([x,0])
  #  print(movements)

class bishop(piece): #Klass för löpare med möjliga drag
    symbol = 'B'
    movements = []
    for x in range(-8,8): 
        movements.append([x,x])
        movements.append([x,-x])
        movements.append([-x,x])
        movements.append([-x,-x])

class knight(piece): #Klass för springare med möjliga drag
    symbol = 'N'
    movements = [[1,2],[-1,2],[1,-2],[-1,-2],[2,1],[2,-1],[-2,-1],[-2,1]]
    #print(movements)

class pawn(piece): #Klass för bonde med möjliga drag
    symbol = 'P'
    movements = [[0,-1], [0,1]]

class meny():
    input

def make2dList(rows, cols): #Skapar en 2d-lista
    return [ ([0] * cols) for row in range(rows) ]

def main():
    b = board(8, 8) #objekt av klassen board -> Objektorienterad-programmering;):* 
    g = game(b) #objekt av klassen game      -^
    g.startGame()
    
if __name__ == "__main__":
    main()