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


    def checkwin(self, char, x, y):
        #check column win
        col=self.cols[x]
        for j in range(height-3):
            if (col[j+0]==char and
                col[j+1]==char and
                col[j+2]==char and
                col[j+3]==char    ):
                return True
        
        #check row win
        for j in range(width-3):
            if (self.cols[j+0][y]==char and
                self.cols[j+1][y]==char and
                self.cols[j+2][y]==char and
                self.cols[j+3][y]==char    ):
                return True

        for i in range(-3,1):
            if (x+i in range(width) and x+i+3 in range(width) and
                y+i in range(height) and y+i+3 in range(height)  ):
                if (self.cols[x+i][y+i]==char and
                    self.cols[x+i+1][y+i+1]==char and
                    self.cols[x+i+2][y+i+2]==char and
                    self.cols[x+i+3][y+i+3]==char):
                    return True
            if (x-i in range(width) and x-i-3 in range(width) and
                y+i in range(height) and y+i+3 in range(height)  ):
                if (self.cols[x-i][y+i]==char and
                    self.cols[x-i-1][y+i+1]==char and
                    self.cols[x-i-2][y+i+2]==char and
                    self.cols[x-i-3][y+i+3]==char    ):
                    return True
        return False

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
        res += f'gameid: {self.gameid}\n'
        try:
            res += f'Turn: {self.currentPlayer.name} ({self.currentPiece})\n\n'
        except:
            res += f'Turn: {self.currentPiece}\n\n'
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
        placed = self.cols[col]
        for i in range(height-1,-1,-1):
            if placed[i]==blank:
                placed[i]=self.currentPiece
                if self.checkwin(self.currentPiece, col, i):
                    if self.currentPiece == red:
                        self.state = 'Red has won!'
                    else:
                        self.state = 'Yellow has won!'
                elif self.checkdraw():
                    self.state = 'The game has drawn!'
                    
                self.game += str(col)
                self.togglePiece()
                self.updatePlayer()
                return True
        return False

    def updatePlayer(self):
        self.currentPlayer = self.p1 if (self.currentPiece == red) else self.p2
    
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
        
class fakeplayer:
    def __init__(self, name):
        self.name = name
    
