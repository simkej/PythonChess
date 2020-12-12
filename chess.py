'''P-uppgift, spelar schack'''
import os


class board:                                                #Class för att skapa spelbrädet

    def __init__(self, xSize, ySize):

        self.xSize = xSize
        self.ySize = ySize

        self.boardObj = make2dList(self.xSize, self.ySize)

        for y in range(0, self.ySize):
            for x in range(0, self.xSize):
                self.set(x, y, piece("none"))

    def printBoard(self):                                   #Skriver ut brädet
        cls()
        for x in self.boardObj:
            line = ""      
            for i in x:
                line += i.symbol
            print(line)

    def printLegalMoves(self, moves):                       #Skriver ut möjliga drag som kan göras
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
            

    def get(self, xPos, yPos):                              #Hämtar nuvarande position i lista
        try:
            return self.boardObj[yPos][xPos]
        except IndexError:
            return #Fixa error-meddelande

    def set(self, xPos, yPos, value):                       #Placerar ut ny position
        self.boardObj[yPos][xPos] = value

class game:

    def __init__(self, board):

        self.board = board
        self.currentTeam = "vit"
    
    def move(self, xOrg, yOrg, xNew, yNew):                 #Förflyttar pjäs, mha get och set.
        legalmove = self.legalmove(xOrg, yOrg)
        wantedmove = [xNew, yNew]
        if wantedmove in legalmove:
            movingPiece = self.board.get(xOrg, yOrg)            
            self.board.set(xOrg, yOrg, piece("none"))
            self.board.set(xNew, yNew, movingPiece)
        else:
            print("Ej lagligt drag")
            return False
            

    def legalmove(self, xOrg, yOrg):                        #Bestämmer lagliga moves för pieces
        piece = self.board.get(xOrg, yOrg)
        moves = []
        upptagen = []
        motståndare = []
        XY = []
        Xy = []
        xY = []
        xy = []
        x_y = []
        x_Y = []
        NewMoves = []
        for i in piece.movements:
            if self.board.get(xOrg+i[0],yOrg+i[1]) is not None and int(xOrg+i[0])>-1 and int(yOrg+i[1])>-1 and [xOrg,yOrg] != [xOrg+i[0],yOrg+i[1]]:
                moves.append([xOrg+i[0],yOrg+i[1]])
                moves.sort()

                if self.board.get(xOrg+i[0],yOrg+i[1]).team != "none":
                    if self.board.get(xOrg+i[0],yOrg+i[1]).team != self.currentTeam:
                        motståndare.append([xOrg+i[0],yOrg+i[1]])
                        
                    if self.board.get(xOrg+i[0],yOrg+i[1]).team == self.currentTeam:
                        upptagen.append([xOrg+i[0],yOrg+i[1]])

        for i in piece.attack:
            if self.board.get(xOrg+i[0],yOrg+i[1]) is not None and int(xOrg+i[0])>-1 and int(yOrg+i[1])>-1 :
               if self.board.get(xOrg+i[0],yOrg+i[1]).team != "none":
                   if self.board.get(xOrg+i[0],yOrg+i[1]).team != self.currentTeam:
                    moves.append([xOrg+i[0],yOrg+i[1]])

        for pos in moves:
            if [xOrg] > [pos[0]]:
                if [yOrg] > [pos[1]]:
                    XY.append(pos)
                if [yOrg] < [pos[1]]:
                    Xy.append(pos)
            if [xOrg] < [pos[0]]:
                if [yOrg] > [pos[1]]:
                    xY.append(pos)
                if [yOrg] < [pos[1]]:
                    xy.append(pos)
            else:
                if [yOrg] > [pos[1]]:
                    x_Y.append(pos)
                if [yOrg] < [pos[1]]:
                    x_y.append(pos)

        XY.sort()
        Xy.sort()
        xY.sort()
        xy.sort()
        x_Y.sort()
        x_y.sort()
                    
        NewMoves += self.kolla(xOrg, yOrg, XY[::-1], motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, Xy[::-1], motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, xY, motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, xy, motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, x_Y, motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, x_y[::-1], motståndare, upptagen)
        
        moves = NewMoves
        return moves

    def kolla(self, xOrg, yOrg, li, motståndare, upptagen):
        NewMoves = []
        for pos in li:
            if pos in motståndare:
                NewMoves.append(pos)
                break
            if pos in upptagen:
                break
            else:
                NewMoves.append(pos)
        return NewMoves

    def isCheckMate(self):
        Hot = []
        HotMove = []
        x = -1
        y = -1
        for brede in self.board.boardObj:
            y += 1
            x = -1
            for piece in brede:
                x += 1
                if piece.team != self.currentTeam and piece.team != "none":
                    Hot.append([x,y])
                if piece.team == self.currentTeam:
                    continue
        for piece in Hot:
            HotMove += self.legalmove(piece[0],piece[1])
            

        
                
                
        #print('Grattis!')
        #self.playing = False
    
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
            board.set(self.board, x, self.board.ySize-2, pawnV("vit"))

        board.set(self.board, 0, 7, rook("vit"))            #Placerar resterande vita pjäser
        board.set(self.board, 1, 7, knight("vit"))
        board.set(self.board, 2, 7, bishop("vit"))
        #print(self.board.get(2,7))
        board.set(self.board, 3, 7, queen("vit"))
        board.set(self.board, 4, 7, king("vit"))
        board.set(self.board, 5, 7, bishop("vit"))
        board.set(self.board, 6, 7, knight("vit"))
        board.set(self.board, 7, 7, rook("vit"))

    def commandInput(self):                                 #Tar inputs från användare.
        posOrg = ''
        oldPos = ''
        command = ''
        command = input("Vad vill "+self.currentTeam+" göra?(move, help eller stop): ")
            
        if command == "move":                               #Hanterar förflyttning av pjäser.
            posOrg = input("Position av pjäs du vill flytta: ")

            if ',' in posOrg:
                oldPos = posOrg.split(',')
                if self.board.get(int(oldPos[0]), int(oldPos[1])).team == self.currentTeam:
                    if len(self.legalmove(int(oldPos[0]),int(oldPos[1]))) != 0:
                        self.board.printLegalMoves(self.legalmove(int(oldPos[0]),int(oldPos[1])))
                    else:
                        print('inga lagliga drag tillgängliga')
                        return False
                else:
                    print("Inte din pjäs att flytta. -2")
                    return False
            else:
                print("Fel formattering, glöm inte ','")
                return False
            
            posNew = input("Positionen du vill flytta den till: ")

            if ',' in posNew:
                newPos = posNew.split(',')
                try:
                    self.move(int(oldPos[0]), int(oldPos[1]), int(newPos[0]), int(newPos[1]))
                except IndexError:
                    print("Värdet är utanför brädet. -4")
                  #  posNew = input("Positionen du vill flytta den till: ")
                except ValueError:
                    print("Ogiltigt val. -5")
                    return False
                    #posNew = input("Positionen du vill flytta den till: ")
            else:
                print("Ogiltigt val. -3")
                return False

        elif command == "help":                               #Visar instruktioner
            print("'move', anger vilken pjäs du vill flytta och vart. \nförsta koordinaten anger kolonn och andra rad, räkning från 0 till 7. \nExempelvis väljs bonden framför vits kung genom '4,6'  \n'stop', avslutar programmet \n ")
            oldPos = ''
            return False

        elif command == "stop":                               #Avslutar programmet
            self.playing = False

        else:
            print("Felaktigt val")
            return False

        return True

    def VitTurn(self):                                      #Kontrollerar om det är vits tur att spela
        self.currentTeam = "vit"
        self.board.printBoard()
        self.isCheckMate()
        while self.commandInput() == False:
            continue
        
    def SvartTurn(self):                                    #Kontrollerar om det är svarts tur att spela
        self.currentTeam = "svart"
        self.board.printBoard()
        self.isCheckMate()
        while self.commandInput() == False:
            continue


    def startGame(self):                                    #Startar spelet
        self.playing = True
        self.placeSvart()
        self.placeVit()

        while self.playing:
            if self.playing:
                self.VitTurn()
            if self.playing:
                self.SvartTurn()

class piece:                                                #Kontrollerar färg, samt hjälper att rensa efter flyttning.
    symbol = '0'
    movements = []
    attack = []
    def __init__(self, team):
        if team == "svart" or team == "vit" or team == "none":
            self.team = team
        else:
            print(team + " is not a valid team.")

class king(piece):                                          #Klass för kungen med möjliga drag
    symbol = 'K'
    movements = []
    attack = movements
    for x in range(-1,2):
        movements.append([0,x])
        movements.append([x,0])
        movements.append([x,x])
        movements.append([x,-x])
        movements.append([-x,x])
        movements.append([-x,-x])
        #if team == 'vit":      Möjlig if-sats för att styra färg direkt i klassen? 
        
class queen(piece):                                         #Klass för damen med möjliga drag
    symbol = 'Q'
    movements = []
    attack = movements
    for x in range(-8,8):
        movements.append([0,x])
        movements.append([x,0])
        movements.append([x,x])
        movements.append([x,-x])
        movements.append([-x,x])
        movements.append([-x,-x])

class rook(piece):                                          #Klass för tornet med möjliga drag
    symbol = 'R'
    movements = []
    attack = movements
    for x in range(-8,8):    #fundera om förbättring, för att bli mer scaleable
        movements.append([0,x])
        movements.append([x,0])
    #print(movements)

class bishop(piece):                                        #Klass för löpare med möjliga drag
    symbol = 'B'
    movements = []
    attack = movements
    for x in range(-8,8): 
        movements.append([x,x])
        movements.append([x,-x])
        movements.append([-x,x])
        movements.append([-x,-x])
    
class knight(piece):                                        #Klass för springare med möjliga drag
    symbol = 'N'
    movements = [[1,2],[-1,2],[1,-2],[-1,-2],[2,1],[2,-1],[-2,-1],[-2,1]]
    attack = movements
    #print(movements)

class pawnV(piece):                                         #Klass för bonde med möjliga drag
    symbol = 'p'
    attack = [[1,-1],[-1,-1]]
    movements = [[0,-1],[0,0]]

class pawn(piece):                                          #Klass för bonde med möjliga drag
    symbol = 'P'
    attack = [[1,1],[-1,1]]
    movements = [[0,1],[0,0]]


#class meny():
 #   input

def make2dList(rows, cols): #Skapar en 2d-lista
    return [ ([0] * cols) for row in range(rows) ]

def cls(): #Överflödig? Möjliggör att använda i Windows. Clear för unix.
    os.system('cls' if os.name=='nt' else 'clear')

def main():
    b = board(8, 8) #objekt av klassen board -> Objektorienterad-programmering;):* 
    g = game(b) #objekt av klassen game      -^
    g.startGame()
    
if __name__ == "__main__":
    main()

#__________________________________________________________________________________________
#To do:
# 
#VS-code, python-plugin
#Ett statiskt spelbräde?
#Eventuellt hårdkoda in rutornas namn? ex a12 = [0,6]
    #Buggar:
