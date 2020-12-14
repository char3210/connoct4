
blank = '<:black:588903518912380939>'
red = '<:red:588903539926106112>'
yellow = '<:yellow:588903561149153280>'
height=6
width=7

class c4game:

    def __init__(self):
        self.currentPiece = red
        self.cols=[[blank]*height for i in range(width)]
        
    def place(self, col):
        for i in range(height-1,0,-1):
            if col[i]==blank:
                col[i]=self.currentPiece
                self.togglePiece()
                return True
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
        for i in range(height):
            for j in range(width):
                res += self.cols[j][i]
            res += '\n'
        return res


    def checkwin(self, char):
        #check column win
        for i in range(width):
            col=self.cols[i]
            for j in range(height-3):
                if (col[j]==char and col[j+1]==char and
                    col[j+2]==char and col[j+3]==char):
                    return True
        
        #check row win
        for i in range(height):
            for j in range(width-3):
                if (self.cols[j][i]==char and self.cols[j+1][i]==char and
                    self.cols[j+2][i]==char and self.cols[j+3][i]==char) :
                    return True
            

        #check diagonal win
        for i in range(height-3):
            for j in range(width-3):
                if ( (self.cols[j][i]==char and self.cols[j+1][i+1]==char and
                      self.cols[j+2][i+2]==char and self.cols[j+3][i+3]==char) or
                     (self.cols[len(self.cols)-j-1][i]==char and self.cols[len(self.cols)-j-2][i+1]==char and
                      self.cols[len(self.cols)-j-3][i+2]==char and self.cols[len(self.cols)-j-4][i+3]==char) ):
                    return True

    def checkdraw(self):
        #check draw
        for i in range(width):
            if self.cols[i][0] == blank:
                return False
        return True



    def clear(self):
        for col in self.cols:
            for p in range(height):
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
        if user==self.p1:
            return 1
        elif user==self.p2:
            return 2
        else:
            return False

    async def clear(self):
        super().clear()
        self.p1 = None
        self.p2 = None
        try:
            await board.delete()
        except:
            pass
        self.board = None

    async def resend(self):
        tb = await self.board.channel.send(self.getboard())
        try:
            await self.board.delete()
        except:
            pass
        self.board = tb
        for x in range(1,8):
            await self.board.add_reaction(f'{x}\uFE0F\u20E3')
        await self.board.add_reaction('\u23F9\uFE0F')
        await self.board.add_reaction('\U0001F501')
        
    
    


