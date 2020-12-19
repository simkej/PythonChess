'''P-uppgift, ett förenklat schack-spel som '''
import os
import copy

class board:
    '''Class för att skapa samt rita brädet'''

    def __init__(self, xSize, ySize):
        '''Skapar brädet'''
        self.xSize = xSize
        self.ySize = ySize
        self.boardObj = make2dList(self.xSize, self.ySize)
        for y in range(0, self.ySize):
            for x in range(0, self.xSize):
                self.set(x, y, piece("none"))

    def printBoard(self):
        '''Skriver ut brädet'''
        for x in self.boardObj:
            line = ""      
            for i in x:
                line += i.symbol
            print(line)

    def printLegalMoves(self, moves):
        '''Skriver ut möjliga drag som kan göras'''
        ursprBoard = []
        for x in moves:
            if self.get(int(x[0]),int(x[1])).symbol != 'X':
                ursprBoard.append([int(x[0]),int(x[1]),self.get(int(x[0]),int(x[1])).symbol])
                self.get(int(x[0]),int(x[1])).symbol = 'X'
        self.printBoard()
        for x in ursprBoard:
            self.get(int(x[0]),int(x[1])).symbol = x[2]       

    def get(self, xPos, yPos):
        '''Hämtar nuvarande position i lista'''
        try:
            return self.boardObj[yPos][xPos]
        except IndexError:
            return #Fixa error-meddelande

    def set(self, xPos, yPos, value):
        '''Placerar ut ny position'''
        self.boardObj[yPos][xPos] = value

class game:
    '''Klass som hanterar spelreglerna, styr förflyttningar och kontrollerar om schack och eller matt uppstår'''
    def __init__(self, board):
        self.board = board
        self.currentTeam = "vit"
    
    def move(self, xOrg, yOrg, xNew, yNew, board):
        '''Förflyttar pjäs, mha get och set.'''
        legalmove = self.legalmove(xOrg, yOrg, self.currentTeam, board)
        wantedmove = [xNew, yNew]
        if wantedmove in legalmove:
            movingPiece = board.get(xOrg, yOrg)            
            board.set(xOrg, yOrg, piece("none"))
            board.set(xNew, yNew, movingPiece)
        else:
            print("Ej lagligt drag")
            return False  

    def legalmove(self, xOrg, yOrg, Team, board):
        '''Bestämmer lagliga moves för pieces genom manipulering och jämförelse av listor.
           Först skapas en lista som populeras av möjliga drag för vald pjäs,
           Sedan två listor med koordinater för alla "motståndare" samt alla "lagkamrater" som står på möjliga drag för pjäsen'''
        piece = board.get(xOrg, yOrg)
        moves = []
        upptagen = []
        motståndare = []
        XY = []
        Xy = []
        xY = []
        xy = []
        X_y = []
        X_Y = []
        Y_x = []
        Y_X = []
        NewMoves = []
        for i in piece.movements:
            if board.get(xOrg+i[0],yOrg+i[1]) is not None and int(xOrg+i[0])>-1 and int(yOrg+i[1])>-1 and [xOrg,yOrg] != [xOrg+i[0],yOrg+i[1]]:
                moves.append([xOrg+i[0],yOrg+i[1]])
                if board.get(xOrg+i[0],yOrg+i[1]).team != "none":     
                    if board.get(xOrg+i[0],yOrg+i[1]).team != Team:
                        motståndare.append([xOrg+i[0],yOrg+i[1]])  
                    if board.get(xOrg+i[0],yOrg+i[1]).team == Team:
                        upptagen.append([xOrg+i[0],yOrg+i[1]])

        for i in piece.attack:
            if board.get(xOrg+i[0],yOrg+i[1]) is not None and int(xOrg+i[0])>-1 and int(yOrg+i[1])>-1 :
               if board.get(xOrg+i[0],yOrg+i[1]).team != "none":
                   if board.get(xOrg+i[0],yOrg+i[1]).team != Team:
                    moves.append([xOrg+i[0],yOrg+i[1]])

        for pos in moves:
            '''Delar upp brädet för att identifiera var andra pjäser står relativt den valda'''
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
            if [xOrg] == [pos[0]]:
                if [yOrg] > [pos[1]]:
                    X_Y.append(pos)
                if [yOrg] < [pos[1]]:
                    X_y.append(pos)
            if [yOrg] == [pos[1]]:
                if [xOrg] > [pos[0]]:
                    Y_X.append(pos)
                if [xOrg] < [pos[0]]:
                    Y_x.append(pos)   

        XY.sort() #De pjäser med x < vald och y < vald
        Xy.sort() #De pjäser med x < vald och y > vald
        xY.sort() #De pjäser med x > vald och y < vald
        xy.sort() #De pjäser med x = vald och y > vald
        X_Y.sort() #De pjäser med x = vald och y < vald
        X_y.sort() #De pjäser med x = vald och y > vald
        Y_X.sort() #De pjäser med x < vald och y = vald
        Y_x.sort() #De pjäser med x > vald och y = vald

        '''Nyttjar kolla-funktionen för att avgöra när en pjäs inte kan gå längre'''
        NewMoves += self.kolla(xOrg, yOrg, XY[::-1], motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, Xy[::-1], motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, xY, motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, xy, motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, X_Y[::-1], motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, X_y, motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, Y_X[::-1], motståndare, upptagen)
        NewMoves += self.kolla(xOrg, yOrg, Y_x, motståndare, upptagen)
        moves = NewMoves
        return moves

    def kolla(self, xOrg, yOrg, li, motståndare, upptagen):
        '''Kontrollerar om någon av rutorna pjäsen kan flyttas till är populerad av motståndare eller egen pjäs
           När en motståndar-pjäs stöts på appendas den positionen så att en fortfarande kan ta den'''
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

    def isCheck(self, board):
        '''kontrollerar om schack uppstått '''
        Hot = []
        Egen = []
        HotMove = []
        EgenMove = []
        kungPos = []
        x = 0
        y = 0
        for brede in board.boardObj:
            x = 0
            for piece in brede:
                if piece.team != self.currentTeam and piece.team != "none":
                    Hot.append([x,y])
                if piece.team == self.currentTeam:
                    Egen.append([x,y])
                    if type(piece) is king:
                        kungPos = [x,y]
                x += 1
            y += 1
        
        for piece in Hot:
            if self.currentTeam == "vit":
                HotMove = HotMove + self.legalmove(piece[0],piece[1], "svart", board)
            if self.currentTeam == "svart":
                HotMove = HotMove + self.legalmove(piece[0],piece[1], "vit", board)

        if self.linsok(HotMove, kungPos):
             return "Schack"
        else:
            return False
        
    def isCheckMate(self, board):
        Egen = []
        EgenMove = []
        counter = 0
        x = 0
        y = 0
        for brede in board.boardObj:
            x = 0
            for piece in brede:
                if piece.team == self.currentTeam:
                    Egen.append([x,y])
                x += 1
            y += 1

        for piece in Egen:
            EgenMove = EgenMove + self.legalmove(piece[0],piece[1], self.currentTeam, board)

        for move in EgenMove:
            board2 = copy.deepcopy(board)
            board2.set(move[0], move[1], pawn(self.currentTeam))
            if self.isCheck(board2) == "Schack":
                continue
            else:
                counter += 1
        if counter == 0:
            return True
              
    def linsok(self, lista, elem): #Anger om givet element finns i listan
        for char in lista:
            if char[0] == elem[0] and char[1] == elem[1]:
                return True
        return False
    
    def placeSvart(self):
        for x in range(0, self.board.xSize):
            '''Placerar ut raden med svarta bönder'''
            board.set(self.board, x, 1, pawn("svart"))
        '''Placerar ut resterande svarta pjäser:'''
        board.set(self.board, 0, 0, rook("svart"))          
        board.set(self.board, 1, 0, knight("svart"))
        board.set(self.board, 2, 0, bishop("svart"))
        board.set(self.board, 3, 0, queen("svart"))
        #board.set(self.board, 1, 2, king("svart"))
        board.set(self.board, 4, 0, king("svart"))
        board.set(self.board, 5, 0, bishop("svart"))
        board.set(self.board, 6, 0, knight("svart"))
        board.set(self.board, 7, 0, rook("svart"))
                
    def placeVit(self):
        for x in range(0, self.board.xSize):
            '''Placerar ut raden med vita bönder'''
            board.set(self.board, x, self.board.ySize-2, pawnV("vit"))
        '''Placerar ut resterande vita pjäser:'''
        board.set(self.board, 0, 7, rook("vit"))            
        board.set(self.board, 1, 7, knight("vit"))
        board.set(self.board, 2, 7, bishop("vit"))
        board.set(self.board, 3, 7, queen("vit"))
        #board.set(self.board, 3, 2, queen("vit"))
        #board.set(self.board, 2, 3, queen("vit"))
        board.set(self.board, 4, 7, king("vit"))
        board.set(self.board, 5, 7, bishop("vit"))
        board.set(self.board, 6, 7, knight("vit"))
        board.set(self.board, 7, 7, rook("vit"))

    def commandInput(self):
        '''Tar inputs från användare.'''
        if self.isCheckMate(self.board) == True:
            print('Schack-Matt!' + self.currentTeam + ' förlorar wää :/')
            self.playing = False
            return True
        if self.isCheck(self.board) == "Schack": 
            print(self.currentTeam + ' är i Schack!') 
        board2 = copy.deepcopy(self.board)
        posOrg = ''
        oldPos = ''
        command = ''
        command = input("Vad vill "+self.currentTeam+" göra?(move, help eller stop): ")
        
        if command == "move":
            '''Hanterar förflyttning av pjäser.'''
            posOrg = input("Position av pjäs du vill flytta: ")
            
            if ',' in posOrg:
                oldPos = posOrg.split(',')
                if self.board.get(int(oldPos[0]), int(oldPos[1])).team == self.currentTeam:
                    if len(self.legalmove(int(oldPos[0]),int(oldPos[1]), self.currentTeam, self.board)) != 0:
                        self.board.printLegalMoves(self.legalmove(int(oldPos[0]),int(oldPos[1]), self.currentTeam, self.board))
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
                    self.move(int(oldPos[0]), int(oldPos[1]), int(newPos[0]), int(newPos[1]), board2)
                    if self.isCheck(board2) == False:
                        print('knark')
                        return self.move(int(oldPos[0]), int(oldPos[1]), int(newPos[0]), int(newPos[1]), self.board)
                    else:
                        print('Du är i schack simon')
                        return False
                except IndexError:
                    print("Värdet är utanför brädet. -4")
                    return False
                except ValueError:
                    print("Ogiltigt val. -5")
                    return False    
            else:
                print("Ogiltigt val. -3")
                return False

        elif command == "help":
            '''Visar instruktioner'''
            print("Detta program kör en förenklad version av schack, alla pjäser kan röra sig som vanligt men vissa features saknas, dessa är: \nEn passant, Rockad och bondens första två steg.\n'move', anger vilken pjäs du vill flytta och vart. \nförsta koordinaten anger kolonn och andra rad, räkning från 0 till 7. \nExempelvis väljs bonden framför vits kung genom '4,6'  \n'stop', avslutar programmet \n ")
            return False

        elif command == "stop":
            '''Avslutar programmet'''
            self.playing = False

        else:
            print("Felaktigt val")
            return False
        return True

    def VitTurn(self):
        '''Kontrollerar om det är vits tur att spela'''
        self.currentTeam = "vit"
        self.board.printBoard()
        while self.commandInput() == False:
            continue
        
    def SvartTurn(self):
        '''Kontrollerar om det är svarts tur att spela'''
        self.currentTeam = "svart"
        self.board.printBoard()
        while self.commandInput() == False:
            continue

    def startGame(self):
        '''Startar spelet'''
        self.playing = True
        self.placeSvart()
        self.placeVit()
        while self.playing:
            if self.playing:
                self.VitTurn()
            if self.playing:
                self.SvartTurn()

class piece:
    '''Kontrollerar färg, samt hjälper att rensa efter flyttning.'''
    symbol = '0'
    movements = []
    attack = []
    def __init__(self, team):
        if team == "svart" or team == "vit" or team == "none":
            self.team = team
        else:
            print(team + " is not a valid team.")

class king(piece):
    '''Klass för kungen med möjliga drag'''
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
        
class queen(piece):
    '''Klass för damen med möjliga drag'''
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

class rook(piece):
    '''Klass för tornet med möjliga drag'''
    symbol = 'R'
    movements = []
    attack = movements
    for x in range(-8,8):    #fundera om förbättring, för att bli mer scaleable
        movements.append([0,x])
        movements.append([x,0])

class bishop(piece):
    '''Klass för löpare med möjliga drag'''
    symbol = 'B'
    movements = []
    attack = movements
    for x in range(-8,8): 
        movements.append([x,x])
        movements.append([x,-x])
        movements.append([-x,x])
        movements.append([-x,-x])
    
class knight(piece):
    '''Klass för springare med möjliga drag'''
    symbol = 'N'
    movements = [[1,2],[-1,2],[1,-2],[-1,-2],[2,1],[2,-1],[-2,-1],[-2,1]]
    attack = movements

class pawnV(piece):
    '''Klass för specifikt vit bonde med möjliga drag'''
    symbol = 'p'
    attack = [[1,-1],[-1,-1]]
    movements = [[0,-1],[0,0]]

class pawn(piece):
    '''Klass för bonde med möjliga drag'''
    symbol = 'P'
    attack = [[1,1],[-1,1]]
    movements = [[0,1],[0,0]]

def make2dList(rows, cols):
    '''Skapar en 2d-lista, behövs för att skapa brädet'''
    return [ ([0] * cols) for row in range(rows) ]

def cls():
    '''Möjliggör att använda i os'''
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
#Schack-matt
#Ett statiskt spelbräde?
#Eventuellt hårdkoda in rutornas namn? ex a12 = [0,6]
    #Buggar:
