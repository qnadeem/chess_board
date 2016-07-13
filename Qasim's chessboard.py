from Tkinter import *
import PIL, ImageTk, copy, time

def geticoord(a):    # Takes x col or y row, and returns where the image's top-left corner should be. 
                     # example if row 1, col 1, then image should be placed at 72ndx72nd pixel.
    if a == 0: return 0
    elif a == 1: return 72
    elif a == 2: return 72*2
    elif a == 3: return 72*3
    elif a == 4: return 72*4
    elif a == 5: return 72*5
    elif a == 6: return 72*6
    elif a == 7: return 72*7

def displaypieces():   # displays all pieces. allimagetags dictionary contains tags of all pieces with keys as tuples: (piece, y,x)!
    global chessboard   # ***  REFERENCE: Images taken from http://ixian.com/chess/jin-piece-sets/
    global allimagetags
    global BRi, BNi, BQi, BPi, BKi, BBi, WRi, WNi, WQi, WPi, WKi, WBi

    for y in range(8):
        for x in range(8):
            if chessboard[y][x] != '0':
                imm = None           # This will be chosen as the correct global image variable in the conditions below.
                if chessboard[y][x] == 'BB': imm = BBi
                if chessboard[y][x] == 'BR': imm = BRi  
                if chessboard[y][x] == 'BN': imm = BNi  
                if chessboard[y][x] == 'BK': imm = BKi  
                if chessboard[y][x] == 'BQ': imm = BQi  
                if chessboard[y][x] == 'BP': imm = BPi  
                if chessboard[y][x] == 'WB': imm = WBi
                if chessboard[y][x] == 'WR': imm = WRi  
                if chessboard[y][x] == 'WN': imm = WNi  
                if chessboard[y][x] == 'WK': imm = WKi  
                if chessboard[y][x] == 'WQ': imm = WQi  
                if chessboard[y][x] == 'WP': imm = WPi

                allimagetags[(chessboard[y][x],y,x)] = c.create_image(geticoord(x), geticoord(y), anchor = NW, image = imm)

def displayrects():  # Make RECTS at validmoves.
    global validmoves, allrects, chessboard, turn

    if len(validmoves) == 0: return None

    for i in validmoves:  # rectangles = the number of valid moves.

        # 'i' is a tuple with (y,x) as a valid move. i[0] = y, i[1] = x 
        if chessboard[i[0]][i[1]] == '0':    # EMPTY square.

            y = geticoord(i[0])
            x = geticoord(i[1])

            recttag = c.create_rectangle(x,y,x+72, y+72, outline = "lawn green", width = 5)
            allrects.append(recttag)

        else:   # CAPTURE!

            y = geticoord(i[0])
            x = geticoord(i[1])

            recttag = c.create_rectangle(x,y,x+72, y+72, outline = "red", width = 5)
            allrects.append(recttag)

def createchesslist(): # Create a 8x8 2-D chessboard list, with all positions filled with the appropriate pieces. For empty places, put 0. 
	chessboard = []
	for i in range(8): chessboard.append(["0"]*8)     
 
	chessboard[0][0] = "BR"
	chessboard[0][1] = "BN"
	chessboard[0][2] = "BB"
	chessboard[0][3] = "BQ"
	chessboard[0][4] = "BK"
	chessboard[0][5] = "BB"
	chessboard[0][6] = "BN"
	chessboard[0][7] = "BR"
	for i in range(8): chessboard[1][i] = "BP"

	chessboard[7][0] = "WR"
	chessboard[7][1] = "WN"
	chessboard[7][2] = "WB"
	chessboard[7][3] = "WQ"
	chessboard[7][4] = "WK"
	chessboard[7][5] = "WB"
	chessboard[7][6] = "WN"
	chessboard[7][7] = "WR"
	for i in range(8): chessboard[6][i] = "WP"

	return chessboard

def getrowcol(y,x):
    # First check which column we clicked in meaning check 'x'.
     if x <=72: col = 0
     elif x <= 72*2: col = 1
     elif x <= 72*3: col = 2
     elif x <= 72*4: col = 3
     elif x <= 72*5: col = 4
     elif x <= 72*6: col = 5
     elif x <= 72*7: col = 6
     elif x <= 72*8: col = 7

     # Now we check 'y', and find which row was clicked in.
     if y <=72: row = 0
     elif y <= 72*2: row = 1
     elif y <= 72*3: row = 2
     elif y <= 72*4: row = 3
     elif y <= 72*5: row = 4
     elif y <= 72*6: row = 5
     elif y <= 72*7: row = 6
     elif y <= 72*8: row = 7

     return row,col

def getbpawnmoves(p, chessboard):    # p is a tuple : (piece, y,x)

    validmoves = []  # append valid moves to this as tuples.
    row = p[1]
    col = p[2]

    if row == 1:  # pawn hasn't moved yet.
        if chessboard[2][col] == '0':
            validmoves.append((2,col))
        if (chessboard[2][col] == '0') and (chessboard[3][col] == '0'):
            validmoves.append((3,col))

    elif (row<=6) and (row>=2):
        if chessboard[row+1][col] == '0':
            validmoves.append((row+1, col))

    # Now check CAPTURES.
    if col == 0 and row<=6:
        if chessboard[row+1][col+1][0] == "W": # a WHITE piece is diagnol to the pawn, so it can be captured!!!
            validmoves.append((row+1,col+1))
    elif col == 7 and row<=6:
        if chessboard[row+1][col-1][0] == "W":
            validmoves.append((row+1,col-1))

    elif col>=1 and col<=6 and row<=6:
        if chessboard[row+1][col+1][0] == "W":
            validmoves.append((row+1, col+1))
        if chessboard[row+1][col-1][0] == "W":
            validmoves.append((row+1,col-1))

    return validmoves

def getwpawnmoves(p,chessboard):  # p is a tuple (piece, y,x)

    validmoves = []  # append valid moves to this as tuples.
    row = p[1]
    col = p[2]

    if row == 6:  # pawn hasn't moved yet.
        if chessboard[5][col] == '0':
            validmoves.append((5,col))
        if (chessboard[5][col] == '0') and (chessboard[4][col] == '0'):  # If both spaces are empty then a pawn can move move 1 or two spaces on its first move.
            validmoves.append((4,col))
    elif (row<=5) and (row>=1):
        if chessboard[row-1][col] == '0':
            validmoves.append((row-1, col))

    # Now check CAPTURES.
    if col == 0 and row>=1:
        if chessboard[row-1][col+1][0] == "B": # a BLACK piece is diagnol to the pawn, so it may be captured!!
            validmoves.append((row-1,col+1))
    elif col == 7 and row>=1:
        if chessboard[row-1][col-1][0] == "B":
            validmoves.append((row-1,col-1))

    elif col>=1 and col<=6 and row>=1:
        if chessboard[row-1][col+1][0] == "B":
            validmoves.append((row-1, col+1))
        if chessboard[row-1][col-1][0] == "B":
            validmoves.append((row-1,col-1))

    return validmoves

def getrookmoves(p,chessboard):
    global turn

    if turn == "W": opponet = "B"
    else: opponet = "W" 

    validmoves = []
    row = p[1]  # Remember 'p' is a tuple for the selected piece such as ("WR", 4, 3)
    col = p[2]

    ## A rook can move in 4 different directions. UP, DOWN, LEFT, RIGHT. 
    ## I will check for all those using 4 loops.

    ### First checking all moves within the same column!!
    y = row + 1    # don't want reference assignment.
    while y<=7:   
      
        if chessboard[y][col] == "0": # if empty space, append to valid move and go to the next square in col.
            validmoves.append((y,col))
            y = y+1
        elif chessboard[y][col][0] == opponet:  # rook can capture opponet piece.
            validmoves.append((y,col))
            y = y+8   # rook can't JUMP over opponet's piece so stop here.
            # the above statement breaks the loop.
        elif chessboard[y][col][0] == turn:
            y = y+8   # rook can't move to or jump over allied piece. 

    y = row - 1
    while y >= 0:
        if chessboard[y][col] == "0": # if empty space, append to valid move and go to the next square in col.
            validmoves.append((y,col))
            y = y-1
        elif chessboard[y][col][0] == opponet:  # rook can capture opponet piece.
            validmoves.append((y,col))
            y = y-8   # rook can't JUMP over opponet's piece so stop here.
        elif chessboard[y][col][0] == turn:
            y = y-8   # rook can't move to or jump over allied piece.


    ### Now check all moves in the same row!! 
    x = col + 1
    while x<=7:

        if chessboard[row][x] == "0": # if empty space, append to valid move and go to the next square in col.
            validmoves.append((row,x))
            x = x+1
        elif chessboard[row][x][0] == opponet:  # rook can capture opponet piece.
            validmoves.append((row,x))
            x = x+8   # rook can't JUMP over opponet's piece so stop here.
        elif chessboard[row][x][0] == turn:
            x = x+8   # rook can't move to or jump over allied piece.

    x = col -1
    while x>=0:

        if chessboard[row][x] == "0": # if empty space, append to valid move and go to the next square in col.
            validmoves.append((row,x))
            x = x-1
        elif chessboard[row][x][0] == opponet:  # rook can capture opponet piece.
            validmoves.append((row,x))
            x = x-8   # rook can't JUMP over opponet's piece so stop here.
        elif chessboard[row][x][0] == turn:
            x = x-8   # rook can't move to or jump over allied piece.


    return validmoves

def getbishopmoves(p,chessboard):
    global turn 

    if turn == "W": opponet = "B"  # Looking at turn and setting the opposite as opponet!
    else: opponet = "W" 

    validmoves = []
    row = p[1]
    col = p[2]

    # A bishop can also move in 4 different directions on the two diagonals, so I check them one by one. 

    y = row+1
    x = col+1    
    while x<=7 and y<=7:
      if chessboard[y][x] == "0": # if empty space, append to valid move and go to the next square in col.
            validmoves.append((y,x))
            x += 1
            y += 1
      elif chessboard[y][x][0] == opponet:  # bishop can capture opponet piece.
            validmoves.append((y,x))
            x += 8   # bishop can't JUMP over opponet's piece so stop here. this statement breaks the loop.
      elif chessboard[y][x][0] == turn:
            x += 8   # bishop can't move to or jump over allied piece.
    
    y = row-1
    x = col-1
    while x>=0 and y>=0:

      if chessboard[y][x] == "0": # if empty space, append to valid move and go to the next square in col.
            validmoves.append((y,x))
            x -= 1
            y -= 1
      elif chessboard[y][x][0] == opponet:  # bishop can capture opponet piece.
            validmoves.append((y,x))
            x -= 8   # bishop can't JUMP over opponet's piece so stop here. this statement breaks the loop.
      elif chessboard[y][x][0] == turn:
            x -= 8   # bishop can't move to or jump over allied piece.

    y = row+1
    x = col-1
    while x>=0 and y<=7:

        if chessboard[y][x] == "0": # if empty space, append to valid move and go to the next square in col.
            validmoves.append((y,x))
            x -= 1
            y += 1
        elif chessboard[y][x][0] == opponet:  # bishop can capture opponet piece.
            validmoves.append((y,x))
            x -= 8   # bishop can't JUMP over opponet's piece so stop here. this statement breaks the loop.
        elif chessboard[y][x][0] == turn:
            x -= 8   # bishop can't move to or jump over allied piece.

    y = row-1
    x = col+1
    while x<=7 and y>=0:

        if chessboard[y][x] == "0": # if empty space, append to valid move and go to the next square in col.
            validmoves.append((y,x))
            x += 1
            y -= 1
        elif chessboard[y][x][0] == opponet:  # bishop can capture opponet piece.
            validmoves.append((y,x))
            x += 8   # bishop can't JUMP over opponet's piece so stop here. this statement breaks the loop.
        elif chessboard[y][x][0] == turn:
            x += 8   # bishop can't move to or jump over allied piece.

    return validmoves

def getqueenmoves(p,c):
    # Queen moves are just the rook and bishop moves combined. So,
    queenmoves = getbishopmoves(p,c) + getrookmoves(p,c)
    return queenmoves

def getknightmoves(p, chessboard):
    # A knight can move into the closest square that does not lie on the vertical/horizontal/diaganol.
    # so it makes an L-shaped move.
    validmoves = []
    row = p[1]
    col = p[2]

    # I will find ALL 8 possible moves for the knight and then check if they are within the board, and that an allied piece isn't in that square.
    boardrange = [0,1,2,3,4,5,6,7]

    possiblemoves = [(row-2,col-1), (row-2,col+1), (row+2, col-1), (row+2,col+1), (row-1,col-2), (row+1,col-2), (row-1,col+2), (row+1,col+2)]
    
    for i in possiblemoves:
        if (i[0] in boardrange) and (i[1] in boardrange) and (chessboard[i[0]][i[1]][0] != turn): # if move INSIDE board and square not occupied by allied piece. add to valid moves.
            validmoves.append((i[0],i[1]))

    return validmoves

def getkingmoves(p, chessboard):
    global hasWKmoved, hasBKmoved, hasLWRmoved, hasRWRmoved, hasLBRmoved, hasLBRmoved
    # A king can move 1 square in any direction.
    validmoves = []
    row = p[1]
    col = p[2]

    # I will find ALL 9 possible moves for the king and then check if they are within the board, and that an allied piece isn't in that square.
    boardrange = [0,1,2,3,4,5,6,7]

    possiblemoves = [(row-1,col-1), (row-1,col+1), (row-1, col), (row,col+1), (row,col-1), (row+1,col-1), (row+1,col+1), (row+1,col)]

    for i in possiblemoves:
        if (i[0] in boardrange) and (i[1] in boardrange) and (chessboard[i[0]][i[1]][0] != turn): # if move INSIDE board and square not occupied by allied piece. add to valid moves.
            validmoves.append((i[0],i[1]))

    return validmoves

def getvalidmoves(selected, c):
    # takes a selected piece as a TUPLE: (piece, y, x)
    # and its current location, and finds all valid moves. VERY important function. uses many others.
    piece = selected
    validmoves = None
    
    if piece[0] == "WP":
        validmoves =getwpawnmoves(piece, c)
    elif piece[0] == "BP":
        validmoves =getbpawnmoves(piece,c)

    elif piece[0][1] == "Q":
        validmoves =getqueenmoves(piece,c)
    elif piece[0][1] == "B":
        validmoves =getbishopmoves(piece,c)
    elif piece[0][1] == "R":
        validmoves =getrookmoves(piece,c)
    elif piece[0][1] == "N":
        validmoves =getknightmoves(piece,c)
    elif piece[0][1] == "K":
        validmoves =getkingmoves(piece,c)

    return validmoves  # list with tuples of valid moves.

##################### SPECIAL MOVES' FUNCTIONS  ###############################
# CASTLING:
def CheckCastling():  # This function checks if the KING is in correct position and it has NOT moved before, and either the left rook or the right rook HAS NOT moved. then it
    # calls another specific function to check if the other conditions for castling are met!! See the text file (in the folder) for details on castling.
    global selected, validmoves, hasWKmoved, hasBKmoved, hasLWRmoved, hasRWRmoved, hasLBRmoved, hasRBRmoved
    p = selected

    if (p[0]=="WK") and (p[1]==7) and (p[2]==4) and (not hasWKmoved) and ((not hasLWRmoved) or (not hasRWRmoved)):  # Check WK's castling if these are true.
        checkwhitecastling()
    
    elif (p[0]=="BK") and (p[1]==0) and (p[2]==4) and (not hasBKmoved) and ((not hasLBRmoved) or (not hasRBRmoved)): # BK's in castling position. check other conditions.
        checkblackcastling() 

def checkwhitecastling():   # checks conditions for the king. if the squares from the king to the rook are empty and if THAT rook hasn't moved before.
    global chessboard, hasLWRmoved, hasRWRmoved, validmoves

    if chessboard[7][2]=="0" and chessboard[7][1]=="0" and chessboard[7][3]=="0" and (not hasLWRmoved):
        validmoves.append((7,2))

    if chessboard[7][5]=="0" and chessboard[7][6]=="0" and (not hasRWRmoved):
        validmoves.append((7,6))

def checkblackcastling(): # checks conditions for the king. if the squares from the king to the rook are empty and if THAT rook hasn't moved before.
    global chessboard, hasLBRmoved, hasRBRmoved, validmoves

    if chessboard[0][2]=="0" and chessboard[0][1]=="0" and chessboard[0][3]=="0" and (not hasLBRmoved):
        validmoves.append((0,2))

    if chessboard[0][5]=="0" and chessboard[0][6]=="0" and (not hasRBRmoved):
        validmoves.append((0,6))

###############################################################################
def bishop():  # 4 button commands to choose selection of promoted pawn.
    global PromoteTo
    PromoteTo = "B"
    promote()
def queen():
    global PromoteTo
    PromoteTo = "Q"
    promote()
def rook():
    global PromoteTo
    PromoteTo = "R"
    promote()
def knight():
    global PromoteTo
    PromoteTo = "N"
    promote()

def promote():
    global chessboard, PromoteTo, allimagetags, lastrankpawn
    global BRi, BNi, BQi, BBi, WRi, WNi, WQi, WBi  # All appropriate images that could be needed!

    name = lastrankpawn[0][0]+PromoteTo
    row = lastrankpawn[1]
    col = lastrankpawn[2]

    c.delete(allimagetags[(chessboard[row][col],row,col)])  # Delete pawn's image, then make new piece's image there.

    chessboard[row][col] = name   # Change the pawn to the selected piece

    if name== "BB": imm = BBi
    if name== "BR": imm = BRi  
    if name== "BN": imm = BNi 
    if name== "BQ": imm = BQi 
    if name== "WB": imm = WBi
    if name=="WR": imm = WRi  
    if name=="WN": imm = WNi  
    if name=="WQ": imm = WQi  

    allimagetags[(chessboard[row][col],row,col)] = c.create_image(geticoord(col), geticoord(row), anchor = NW, image = imm)  # Create new image at selected piece.
    
    knightb.place_forget()  # Remove all the promote buttons. We're done!
    queenb.place_forget()
    rookb.place_forget()
    bishopb.place_forget()
    prolabel.place_forget()

def pawnpromotion(piece, row, col):
    global lastrankpawn

    lastrankpawn = (piece,row,col)   # Remember where the lastrankedpawn is.

    prolabel.place(x=595, y= 85) # Place promotion label.
    bishopb.place(x=595, y =190) #Placing the button.
    queenb.place(x=595, y =140) #Placing the button.
    rookb.place(x=685, y =140) #Placing the button.
    knightb.place(x=685, y =190) #Placing the button.

##################### KING SAFETY AND CHECK/CHECKMATE/STALEMATE FUNCTIONS ################
def findking(copyboard):  # Finds the king's square on the board.
    global turn
    king = turn+"K"
    for i in range(8):
        for j in range(8):
            if copyboard[j][i] == king:
                return (j,i)

def iskingincheck():    # If the opponet can attack the king (he can use SOME piece, ANY piece, to reach the king's square!!!!)
                        #  , return True, else return False.
    global chessboard

    kingsquare = findking(chessboard)
    ALL = getallopponetmoves(chessboard)
    if kingsquare in ALL: return "Y"
    else: return "N"

def getallselfmoves(copyboard):  # Similar to the function below but 2 MAJOR changes:
    global turn     # 1) No need to switch turn twice because we're getting our own moves.
                    # 2) Use the checkkingsafety() function so that we can check for each piece, kingsafety as we find it on the board.

    alllegalmoves = []

    for i in range(8):
        for j in range(8):
            piece = copyboard[j][i]

            if piece != "0" and piece[0] == turn:   # turn is OPPOSITION now.
                v = getvalidmoves((copyboard[j][i],j,i), copyboard)

                v = checkkingsafety((copyboard[j][i],j,i), v)
                for x in v:
                    if x not in alllegalmoves:
                        alllegalmoves.append(x)    

    return alllegalmoves

def getallopponetmoves(copyboard):   ##  Get ALL possible moves that the opponet can make.
    global turn

    if turn == "W": turn = "B"
    else: turn = "W"    # I need to change turn just for this emulation, so that I can get valid moves below! I'll change it at
                    # the end of this function!!!! 
    alllegalmoves = []

    for i in range(8):
        for j in range(8):
            piece = copyboard[j][i]

            if piece != "0" and piece[0] == turn:   # turn is OPPOSITION now.
                v = getvalidmoves((copyboard[j][i],j,i), copyboard)
                for x in v:
                    if x not in alllegalmoves:
                        alllegalmoves.append(x)

    if turn =="W": turn = "B"  ## I CHANGE the turn back to the original turn. I flipped the turn twice so I could use the getvalidmoves() 
    else: turn = "W"           # function correctly for this function.

    return alllegalmoves

def checkkingsafety(selected, validmoves):
    global chessboard
    # v is a list of all valid moves returned. Go through each move and see if the KING is in danger, if he is: REMOVE  that move as it is illegal.   

    illegal = []

    for i in validmoves:

        Drow = i[0]
        Dcol = i[1]

        copyboard = copy.deepcopy(chessboard)  # Make DEEP copy of chessboard, and make that move and check if king is threatened.
        # DEEP copy makes sure that the original chessboard list is NOT disturbed. that would mess everything up.

        copyboard[Drow][Dcol] = selected[0]            # I make the move on this copyboard and check if its legal.
        copyboard[selected[1]][selected[2]] = "0" 

        kingsquare = findking(copyboard)  

        ALL = getallopponetmoves(copyboard)

        if kingsquare in ALL: # Meaning the opponet can get to the king.
            illegal.append(i)

    for i in illegal:   # removing the illegal moves from the validmoves list.
        validmoves.remove(i)
    return validmoves
#################################################################################################3

def makethemove(row, col):  #MOVES the selected piece to the destination square. The row,col taken are the destination square.
    global chessboard, selected, allimagetags, turn, hasbeenpromoted, hasLBRmoved,hasRWRmoved,hasLWRmoved, hasRBRmoved, hasBKmoved, hasWKmoved

    piecename = selected[0]
    Crow = selected[1]           # Current row and column.
    Ccol = selected[2]

    Drow = row                   # destination row and column.
    Dcol = col

    ##############################################################################################################
    ## First check if Castling move. Because that's the 'strangest' move, involving moving two pieces.###################
    if piecename=="WK" and (not hasWKmoved) and (Crow,Ccol)==(7,4):    # Is it a WK castling move?
        if (Drow,Dcol)==(7,2): #LEft side castling.
            
            c.coords(allimagetags[selected], geticoord(Dcol), geticoord(Drow))   # IMPORTANT: c.coords takes coordinates as x,y    NOT as y,x.
            # After Moving the image, I CHANGE the key of the image in the dictionary here (in two simple steps.)
            allimagetags[(piecename, Drow, Dcol)] = allimagetags[selected]
            del allimagetags[selected]

            # Now MOVE Left WHITE Rook.
            c.coords(allimagetags[("WR",7,0)], geticoord(3), geticoord(7))
            allimagetags[("WR", 7, 3)] = allimagetags[("WR",7,0)]
            del allimagetags["WR",7,0]

            # Now make actual move.
            chessboard[Drow][Dcol] = selected[0]
            chessboard[Crow][Ccol] = "0"
            chessboard[7][3] = "WR"
            chessboard[7][0] = "0"
            hasWKmoved = True
        
        elif (Drow,Dcol)==(7,6):
            c.coords(allimagetags[selected], geticoord(Dcol), geticoord(Drow))   # IMPORTANT: c.coords takes coordinates as x,y    NOT as y,x.
            # After Moving the image, I CHANGE the key of the image in the dictionary here (in two simple steps.)
            allimagetags[(piecename, Drow, Dcol)] = allimagetags[selected]
            del allimagetags[selected]

            # Now MOVE Left WHITE Rook.
            c.coords(allimagetags[("WR",7,7)], geticoord(5), geticoord(7))
            allimagetags[("WR", 7, 5)] = allimagetags[("WR",7,7)]
            del allimagetags["WR",7,7]

            # Now make actual move.
            chessboard[Drow][Dcol] = selected[0]
            chessboard[Crow][Ccol] = "0"
            chessboard[7][5] = "WR"
            chessboard[7][7] = "0"
            hasWKmoved = True

    elif piecename=="BK" and (not hasBKmoved) and (Crow,Ccol)==(0,4):  ### Is it a Black king castling move?
        if (Drow,Dcol)==(0,2): #LEft side castling.
            
            c.coords(allimagetags[selected], geticoord(Dcol), geticoord(Drow))   # IMPORTANT: c.coords takes coordinates as x,y    NOT as y,x.
            # After Moving the image, I CHANGE the key of the image in the dictionary here (in two simple steps.)
            allimagetags[(piecename, Drow, Dcol)] = allimagetags[selected]
            del allimagetags[selected]

            # Now MOVE Left WHITE Rook.
            c.coords(allimagetags[("BR",0,0)], geticoord(3), geticoord(0))
            allimagetags[("BR", 0, 3)] = allimagetags[("BR",0,0)]
            del allimagetags["BR",0,0]

            # Now make actual move.
            chessboard[Drow][Dcol] = selected[0]
            chessboard[Crow][Ccol] = "0"
            chessboard[0][3] = "BR"
            chessboard[0][0] = "0"
            hasBKmoved = True
        
        elif (Drow,Dcol)==(0,6):
            c.coords(allimagetags[selected], geticoord(Dcol), geticoord(Drow))   # IMPORTANT: c.coords takes coordinates as x,y    NOT as y,x.
            # After Moving the image, I CHANGE the key of the image in the dictionary here (in two simple steps.)
            allimagetags[(piecename, Drow, Dcol)] = allimagetags[selected]
            del allimagetags[selected]

            # Now MOVE Left WHITE Rook.
            c.coords(allimagetags[("BR",0,7)], geticoord(5), geticoord(0))
            allimagetags[("BR", 0, 5)] = allimagetags[("BR",0,7)]
            del allimagetags["BR",0,7]

            # Now make actual move.
            chessboard[Drow][Dcol] = selected[0]
            chessboard[Crow][Ccol] = "0"
            chessboard[0][5] = "BR"
            chessboard[0][7] = "0"
            hasBKmoved = True
    #############################################################################
    # Now check REGULAR moves.
    elif chessboard[Drow][Dcol] == "0": # if destination is an empty square.
        
        # First I move the IMAGE on screen. selected acts as the KEY to the image as well! 
        c.coords(allimagetags[selected], geticoord(Dcol), geticoord(Drow))   # IMPORTANT: c.coords takes coordinates as x,y    NOT as y,x.
        
        # After Moving the image, I CHANGE the key of the image in the dictionary here (in two simple steps.)
        allimagetags[(piecename, Drow, Dcol)] = allimagetags[selected]
        del allimagetags[selected]

        # Now, I make the move in the chessboard list.
        chessboard[Drow][Dcol] = selected[0]
        chessboard[Crow][Ccol] = "0"

    elif (chessboard[Drow][Dcol] != "0"): 
        
        c.coords(allimagetags[selected], geticoord(Dcol), geticoord(Drow))
        allimagetags[(piecename, Drow, Dcol)] = allimagetags[selected]
        del allimagetags[selected]

        # HERE I also need to DELETE the image of the opponet's piece at the Destination square.
        c.delete(allimagetags[(chessboard[Drow][col],Drow,Dcol)])      # I give the imagetag dictionary the destination piece's tuple (name,y,x) and 
                                                                  # delete that image!
        # Now I make the move in the chessboard list.
        chessboard[Drow][Dcol] = selected[0]
        chessboard[Crow][Ccol] = "0"

    # Pawn promotion check-up.    
    if (piecename == "WP" and Drow == 0) or (piecename == "BP" and Drow == 7): # If a pawn reached the last rank (row), activate promotion.
        pawnpromotion(piecename, Drow, Dcol)

    # Castling moves check-up.
    if piecename=="WR" and hasLWRmoved==False and (Crow,Ccol)==(7,0): hasLWRmoved = True
    elif piecename=="WR" and hasRWRmoved==False and (Crow,Ccol)==(7,7): hasRWRmoved = True
    elif piecename=="BR" and hasLBRmoved==False and (Crow,Ccol)==(0,0): hasLWRmoved = True
    elif piecename=="BR" and hasRBRmoved==False and (Crow,Ccol)==(0,7): hasRWRmoved = True
    elif piecename=="WK" and hasWKmoved==False and (Crow,Ccol)==(7,4): hasWKmoved = True
    elif piecename=="BK" and hasBKmoved==False and (Crow,Ccol)==(0,4): hasWKmoved = True

def gameover(x):  ## After the game is over. If king in check: CHECKMATE. if king is not in check (which is rare):  STALEMATE (a draw).
    global turn, gameup

    if turn == "W": winner = "Black"
    else: winner = "White"

    if x == "Y": turnt.set("CHECKMATE.\n"+winner+ " wins.")
    if x == "N": turnt.set("STALEMATE. \nIt's a draw.")
    gameup = True

def mouseclick(e):     # Main controller function. Takes a mouseclick and decides what to do with it! A mouseclick is the only 'event' that
                  # drives all other functions!               
     global turn, selected, validmoves, allrects, allimagetags, turnt, chessboard, gameup
     x = e.x
     y = e.y
     row = None
     col = None

     row, col = getrowcol(y,x)

     clickedon = chessboard[row][col]

     if gameup == True: return None

     if (selected == None) and (clickedon[0] != turn): return None  # If white clicks on black pieces (or vice versa) then dont select it.

     # The person clicked on his OWN piece, so SELECT that piece
     # and GET the valid moves, and MAKE the rectangles.
     elif (clickedon[0] == turn): 
        
        # I delete all valiedmoves. And delete all rectangles (from canvas AND the tags in the list)
        del validmoves[:]
        for i in allrects: c.delete(i)
        del allrects[:]

        selected = (clickedon,row,col)    # SELECT this piece.


        validmoves = getvalidmoves(selected, chessboard)   # this function returns list of tuples
                                                        # with the (row,col) of the valid moving squares. 
        CheckCastling() # Checks if there are castling moves and adds them to validmoves global list.

        validmoves = checkkingsafety(selected, validmoves)

        # Make a rectangle at the SELECTED piece and append tag to allrects.#####
        y = geticoord(row)
        x = geticoord(col)
        recttag = c.create_rectangle(x,y,x+72, y+72, outline = "lawn green", width = 5)
        allrects.append(recttag)
        ########################################################

        displayrects()    # make RECTANGLES at VALIDMOVES. (this function uses the global list -> valid moves.)     

     elif (selected[0][0] == turn) and (clickedon[0]!= turn): # You already selected a piece. Now you click on an empty square or an opponet-occupied square.

          
          if (len(validmoves) == 0) or ((row, col) not in validmoves): 
          # if the box where you clicked isn't a valid move, don't make a move. and deselect the piece, and destroy all rects, and validmoves.
              if len(validmoves) != 0: del validmoves[:]

              for i in allrects: c.delete(i)
              
              del allrects[:]

              selected = None      

          elif (selected[0][0] == turn) and (row, col) in validmoves:   # Remember 'selected' variable is a tuple: (piece, y,x).

              # First remove all the valid move RECTS.
              for i in allrects: c.delete(i)
              del allrects[:]

              #################################################3
              makethemove(row, col)   # This function takes the destination row,col and moves the SELECTED piece to it. 
              #########################  It ALSO moves the image to the dest. square! 

              selected = None  # move's over. change 'selected' back to None.

              # A move has been made. CHANGE TURN.
              if turn == "W": 
                turn = "B"
                turnt.set("Black to move.")
              elif turn == "B": 
                turn = "W"
                turnt.set("White to move.")

              # CHECK for MATE after each turn. So, we check if the person has ANY moves at all. 
              S = getallselfmoves(chessboard)
              if len(S) == 0:  # If the person has no moves, then GAME OVER! Checkmate if king under check; stalemate otherwise.
                winordraw = iskingincheck()
                gameover(winordraw)

def restart():# Reset everything. Make fresh chesslist. make new images. make all variables to their DEFAULT state!!
    global chessboard, allimagetags, turn, selected, allrects, gameup, validmoves, PromoteTo, lastrankpawn 
    global hasLBRmoved,hasRWRmoved,hasLWRmoved, hasRBRmoved, hasBKmoved, hasWKmoved

    for i in allimagetags:  c.delete(allimagetags[i])
    for i in allrects: c.delete(i)
    
    chessboard = createchesslist()
    allimagetags = {}
    turn = "W"
    selected = None
    allrects = []
    validmoves = []
    gameup = False
    PromoteTo = None   # turn to Q/B/N/R
    lastrankpawn = None
    hasWKmoved = False
    hasBKmoved = False
    hasLWRmoved = False
    hasRWRmoved = False
    hasRBRmoved = False
    hasLBRmoved = False

    turnt.set("White to move.")
    displaypieces()

def playgame(): # remove the welcome screen.
    welcomel.place_forget()
    playgameb.place_forget()

root = Tk()
root.geometry("804x594")
root.title("Qasim's Chess") # The root window properties.
root.config(bg = 'dodgerblue4')

c = Canvas(root,height = 576, width = 576,background="white", relief = RAISED)
c.place(x=5,y=5)  # canvas position.

for x in range(8):# This 8x8 loop creates a chessboard where each square is 72x72 pixels. The board is 576x576.
     for i in range(8):
        
        if (x+i)%2 == 1:
             
            c.create_rectangle(72*i, 72*x, 72+72*i, 72+72*x, fill='RosyBrown4')
        else:
            c.create_rectangle(72*i, 72*x, 72+72*i, 72+72*x, fill ='honeydew')

chessboard = createchesslist()  # Create a list for the board.

allimagetags = {} ### The dictionary allimagetags has all piece name strings as values, and their 'create_image' as values. 
                  #   they can be moved using tags later on.

BRi = ImageTk.PhotoImage(file="pieces/BR.png")     # Loading all image files. They are used in the below function "displaypieces".
BNi = ImageTk.PhotoImage(file="pieces/BN.png")    # ***  REFERENCE: Images taken from http://ixian.com/chess/jin-piece-sets/
BBi = ImageTk.PhotoImage(file="pieces/BB.png")
BKi = ImageTk.PhotoImage(file="pieces/BK.png")
BQi = ImageTk.PhotoImage(file="pieces/BQ.png")
BPi = ImageTk.PhotoImage(file="pieces/BP.png")
WRi = ImageTk.PhotoImage(file="pieces/WR.png")
WNi = ImageTk.PhotoImage(file="pieces/WN.png")
WBi = ImageTk.PhotoImage(file="pieces/WB.png")
WKi = ImageTk.PhotoImage(file="pieces/WK.png")
WQi = ImageTk.PhotoImage(file="pieces/WQ.png")
WPi = ImageTk.PhotoImage(file="pieces/WP.png")

displaypieces()   # Displays all chess pieces on the board. Using the chessboard list and the image variables above.

turn = "W"    # White ALWAYS moves first :)
selected = None   # is any piece currently selected by the user? a selected piece will be stored as a tuple like this: (piecename, row, col)
validmoves = []

allrects = []     # contains tags to all rectangles on screen.
gameup = False   # turn to True when game ends.

########### Pawn Promotion Stuff#############
prolabel = Label(root, text = "Promote to: ", font=("Helvetica", 20), bg='white')  # PROMOTE text.
# The four selection buttons
bishopb = Button(root, command=bishop, text="Bishop",font =("Times", 14), highlightthickness= 2, fg ='black', bg = 'light slate gray', relief = RAISED, bd=3)
queenb = Button(root, command=queen, text="Queen",font =("Times", 14), highlightthickness= 2, fg ='black', bg = 'light slate gray', relief = RAISED, bd=3)
rookb = Button(root, command=rook, text="Rook",font =("Times", 14), highlightthickness= 2, fg ='black', bg = 'light slate gray', relief = RAISED, bd=3)
knightb = Button(root, command=knight, text="Knight",font =("Times", 14), highlightthickness= 2, fg ='black', bg = 'light slate gray', relief = RAISED, bd=3)

PromoteTo = None   # turn to Q/B/N/R
lastrankpawn = None
#####################################################
## CASTLING variables.
hasWKmoved = False
hasBKmoved = False
hasLWRmoved = False
hasRWRmoved = False
hasRBRmoved = False
hasLBRmoved = False
################
# TURN label.
turnt = StringVar()
turnt.set("White to move.")  # Day label displays current day. gets changed when 'SELL' is pressed.
turnlabel = Label(root, textvariable = turnt, font=("Times", 22), bg='white', relief = GROOVE)
turnlabel.place(x=595, y=10)

##################
c.bind("<Button-1>",mouseclick)    # MAIN event that calls functions. Only user input is through the left mouse click
##################
restartb = Button(root, command=restart, text="Reset Chessboard",font =("Times", 15), highlightthickness= 2, fg ='red', bg = 'white',relief = RAISED, bd=3)
restartb.place(x=615, y= 530) #Placing the button.

################# Welcome label and button.
welcomei = ImageTk.PhotoImage(file="pieces/img2.png") # REFERENCE: Taken from http://en.downloadswallpapers.com/wallpaper/chess-pieces-13752.htm 
welcomel = Label(root,image = welcomei)
welcomel.place(x=0, y=0)

playgameb = Button(root, command=playgame, text="Play Chess",font =("Helvetica", 23), highlightthickness= 4, fg ='white', bg = 'black',relief = RAISED, bd=3)
playgameb.place(x=220, y=290)
####################
root.mainloop()
