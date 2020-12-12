
blank = '<:black:588903518912380939>'
red = '<:red:588903539926106112>'
yellow = '<:yellow:588903561149153280>'

currentPiece = red
c1=[blank]*6
c2=[blank]*6
c3=[blank]*6
c4=[blank]*6
c5=[blank]*6
c6=[blank]*6
c7=[blank]*6
cols=[c1,c2,c3,c4,c5,c6,c7]

def place(col):
    i = len(col)-1
    while i>=0:
        if col[i]==blank:
            col[i]=currentPiece
            togglePiece()
            return True
        i=i-1
    return False

def togglePiece():
    global currentPiece
    if currentPiece == red:
        currentPiece = yellow
    else :
        currentPiece = red

def getboard():
    res = f'Turn: {currentPiece}\n \n'
    for x in range(1,8):
        res += f'{x}\uFE0F\u20E3'
    res +='\n'
    for i in range(len(c1)):
        for j in range(len(cols)):
            res += cols[j][i]
        res += '\n'
    return res


def checkwin(char):
    #check column win
    for i in range(len(cols)):
        col=cols[i]
        for j in range(len(c1)-3):
            if (col[j]==char and col[j+1]==char and
                col[j+2]==char and col[j+3]==char):
                return True
        
    #check row win
    for i in range(len(c1)):
        for j in range(len(cols)-3):
            if (cols[j][i]==char and cols[j+1][i]==char and
                cols[j+2][i]==char and cols[j+3][i]==char) :
                return True
        

    #check diagonal win
    for i in range(len(c1)-3):
        for j in range(len(cols)-3):
            if ( (cols[j][i]==char and cols[j+1][i+1]==char and
                  cols[j+2][i+2]==char and cols[j+3][i+3]==char) or
                 (cols[len(cols)-j-1][i]==char and cols[len(cols)-j-2][i+1]==char and
                  cols[len(cols)-j-3][i+2]==char and cols[len(cols)-j-4][i+3]==char) ):
                return True

def checkdraw():
    #check draw
    for i in range(len(cols)):
        if cols[i][0] == blank:
            return False
    return True



def clear():
    global cols, currentPiece
    for col in cols:
        for p in range(len(col)):
            col[p]=blank
    
    currentPiece = red



