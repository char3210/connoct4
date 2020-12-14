
blank = '<:black:588903518912380939>'
red = '<:red:588903539926106112>'
yellow = '<:yellow:588903561149153280>'

class c4game:

    def __init__(self):
        self.currentPiece = red
        """
        self.c1=[blank]*6
        self.c2=[blank]*6
        self.c3=[blank]*6
        self.c4=[blank]*6
        self.c5=[blank]*6
        self.c6=[blank]*6
        self.c7=[blank]*6
        self.cols=[self.c1,self.c2,self.c3,self.c4,self.c5,self.c6,self.c7]
        """
        height=6
        width=7
        self.cols=[[blank]*height]*width
        
    def place(self, col):
        i = len(col)-1
        while i>=0:
            if col[i]==blank:
                col[i]=self.currentPiece
                self.togglePiece()
                return True
            i=i-1
        return False

    def togglePiece(self):
        if self.currentPiece == red:
            self.currentPiece = yellow
        else :
            self.currentPiece = red

    def getboard(self):
        res = f'Turn: {self.currentPiece}\n \n'
        for x in range(1,8):
            res += f'{x}\uFE0F\u20E3'
        res +='\n'
        for i in range(len(self.c1)):
            for j in range(len(self.cols)):
                res += self.cols[j][i]
            res += '\n'
        return res


    def checkwin(self, char):
        #check column win
        for i in range(len(self.cols)):
            col=self.cols[i]
            for j in range(len(self.c1)-3):
                if (col[j]==char and col[j+1]==char and
                    col[j+2]==char and col[j+3]==char):
                    return True
        
        #check row win
        for i in range(len(self.c1)):
            for j in range(len(self.cols)-3):
                if (self.cols[j][i]==char and self.cols[j+1][i]==char and
                    self.cols[j+2][i]==char and self.cols[j+3][i]==char) :
                    return True
            

        #check diagonal win
        for i in range(len(self.c1)-3):
            for j in range(len(self.cols)-3):
                if ( (self.cols[j][i]==char and self.cols[j+1][i+1]==char and
                      self.cols[j+2][i+2]==char and self.cols[j+3][i+3]==char) or
                     (self.cols[len(self.cols)-j-1][i]==char and self.cols[len(self.cols)-j-2][i+1]==char and
                      self.cols[len(self.cols)-j-3][i+2]==char and self.cols[len(self.cols)-j-4][i+3]==char) ):
                    return True

    def checkdraw(self):
        #check draw
        for i in range(len(self.cols)):
            if self.cols[i][0] == blank:
                return False
        return True



    def clear(self):
        for col in self.cols:
            for p in range(len(col)):
                col[p]=blank
        
        self.currentPiece = red


class discordgame(c4game):
    def __init__(self, gameid):
        super().__init__()
        self.gameid=gameid
        self.p1 = None
        self.p2 = None
        self.board = None 

    def checkuser(self, user):
        pass
    
        
        
    
    


