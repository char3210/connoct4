import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

import testc4

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='c!')

p1=p2=None
board = None
games=[]
newid=0
game = testc4.c4game()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected')

def getgame(board):
    for g in range(len(games)):
        if board == games[g].board:
            return games[g]
    return None

@bot.event
async def on_reaction_add(reaction, user):
    
    if user.bot:
        return
    
    game = getgame(reaction.message)
    game.checkuser(user)
    
    if (reaction.message==board)==False:
        return
    
    global p1, p2
    if p1==None:
        p1=user
        await reaction.message.channel.send(f"Player 1 has joined: {user.name} ({testc4.red})")
    elif p2==None:
        p2=user
        await reaction.message.channel.send(f"Player 2 has joined: {user.name} ({testc4.yellow})")

    
    try:
        chosen = int(reaction.emoji[0])-1
    except:
        return

    if (user == p1 and game.currentPiece == testc4.red) or (user==p2 and game.currentPiece == testc4.yellow):
        if not game.place(game.cols[chosen]):
                await reaction.message.channel.send("invalid move, next to go is still "+game.currentPiece)
    else :
        await reaction.message.channel.send("It is not your turn!")

    
    await reaction.remove(user)
    await board.edit(content = game.getboard())
    
    if game.checkwin('<:red:588903539926106112>'):
        await reaction.message.channel.send(f"red ({p1.name}) wins!")
        stopgame()
    elif game.checkwin('<:yellow:588903561149153280>'):
        await reaction.message.channel.send(f"yellow ({p2.name}) wins!")
        stopgame()
    elif game.checkdraw():
        await reaction.message.channel.send("the game has drawn!")
        stopgame()
    

@bot.command(name='start')
async def start(ctx):
    global games
    game = discordgame(len(games))
    games.append(game)
    game.board = await ctx.send(game.getboard())
    for x in range(1,8):
        await game.board.add_reaction(f'{x}\uFE0F\u20E3')

@bot.command(name='stop')
async def stopcmd(ctx):
    stopgame()
    await ctx.send('game has been stopped')

def stopgame():
    global p1, p2, board
    game.clear()
    p1=None
    p2=None
    board = None

@bot.command(name='resend')
async def resendBoard(ctx):
    global board
    if not board == None:
        try:
            await board.delete()
        except:
            pass
        board = await ctx.send(game.getboard())
        for x in range(1,8):
            await board.add_reaction(f'{x}\uFE0F\u20E3')
    else:
        await ctx.send('no ongoing game rn')

@bot.command(name='animoji')
async def animoji(ctx):
    print(ctx.message.guild.emojis)
    await ctx.send('<a:yred:787220892853731348>')
    
bot.run(TOKEN)
