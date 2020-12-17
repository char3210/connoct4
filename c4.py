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
        for i in range(height-1,-1,-1):
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
                     (self.cols[-j-1][i]==char and self.cols[-j-2][i+1]==char and
                      self.cols[-j-3][i+2]==char and self.cols[-j-4][i+3]==char) ):
                    return True

    def checkdraw(self):
        #check draw
        for i in range(width):
            if self.cols[i][0] == blank:
                return False
        return True

class discordgame(c4game):
    def __init__(self, gameid):
        super().__init__()
        self.currentPlayer = None
        self.gameid = gameid
        self.p1 = None
        self.p2 = None
        self.board = None
        self.game = ''
        self.state = ''

    def getboard(self):
        res = ''
        try:
            res += f'Turn: {self.currentPlayer.name} ({self.currentPiece})\n'
        except:
            res += f'Turn: {self.currentPiece}\n'
        res += f'gameid: {self.gameid}\n\n'
        for x in range(1,8):
            res += f'{x}\uFE0F\u20E3'
        res +='\n'
        for i in range(height):
            for j in range(width):
                res += self.cols[j][i]
            res += '\n'
        res += self.state
        return res

    def stop(self):
        self.board = None
        f = open('games.txt','a')
        try:
            f.write(f'{self.gameid} {self.p1.name} {self.p2.name} {self.game}\n')
        except:
            f.write(f'{self.gameid} stopped\n')
        f.close()
        self.p1 = None
        self.p2 = None

    def place(self, col):
        success = super().place(self.cols[col])
        if success:
            self.game += str(col)
        self.updatePlayer()
        self.updateState()
        return success

    def updatePlayer(self):
        self.currentPlayer = self.p1 if (self.currentPiece == red) else self.p2
    
    def updateState(self):
        if self.checkwin(red):
            self.state = 'Red has won!'
        elif self.checkwin(yellow):
            self.state = 'Yellow has won!'
        elif self.checkdraw():
            self.state = 'The game has drawn!'
    
    async def say(self, msg):
        await self.board.channel.send(msg)
    
    async def handle(self, col, player):
        if self.p1 == None:
            self.p1 = player
            await self.say(f"Player 1 has joined: {player.name} ({red})")
        elif self.p2 == None:
            self.p2 = player
            await self.say(f"Player 2 has joined: {player.name} ({yellow})")

        self.updatePlayer()
        if (player == self.currentPlayer):
            if not self.place(col):
                await self.say(f"Invalid move! Turn is still {self.currentPlayer.name} ({self.currentPiece})")
        elif (player == self.p1 or player == self.p2):
            await self.say("It is not your turn!")
        else:    
            await self.say("You are not in this game!")
        
        await self.board.edit(content = self.getboard())
        if bool(self.state):
            self.stop()
        
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
        
    
    


