import os
import tracemalloc
import discord

from dotenv import load_dotenv
from discord.ext import commands

import c4

tracemalloc.start()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='c!')

games=[]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected')
    try:
        f = open('games.txt')
    except:
        f = open('games.txt', 'w')
    global newid
    newid = len(f.readlines())
    f.close()

def getboard(board):
    for g in range(len(games)):
        if board == games[g].board:
            return games[g]
    return None

@bot.event
async def on_reaction_add(reaction, user):
    
    if user.bot:
        return
    
    game = getboard(reaction.message)
    if(game == None):
        return
    
    chosen = None
    try:
        chosen = int(reaction.emoji[0])-1
        if (not (chosen in range(0,7))):
            return
        
        if game.p1==None:
            game.p1=user
            await reaction.message.channel.send(f"Player 1 has joined: {user.name} ({c4.red})")
        elif game.p2==None:
            game.p2=user
            await reaction.message.channel.send(f"Player 2 has joined: {user.name} ({c4.yellow})")
    
        if(not bool(game.checkuser(user))):
            await reaction.message.channel.send("You are not in this game!")
            await reaction.remove(user)
            return
        else:
            if (user == game.p1 and game.currentPiece == c4.red) or (user==game.p2 and game.currentPiece == c4.yellow):
                if not game.place(chosen):
                        await reaction.message.channel.send("invalid move, next to go is still "+game.currentPiece)
            else :
                await reaction.message.channel.send("It is not your turn!")

        await game.board.edit(content = game.getboard())
        if game.checkwin(c4.red):
            await reaction.message.channel.send(f"red ({game.p1.name}) wins!")
            await stopgame(game)
        elif game.checkwin(c4.yellow):
            await reaction.message.channel.send(f"yellow ({game.p2.name}) wins!")
            await stopgame(game)
        elif game.checkdraw():
            await reaction.message.channel.send("the game has drawn!")
            await stopgame(game)
    
    except:
        if reaction.emoji == '⏹️':
            await stopgame(game)
            await reaction.message.channel.send('game has been stopped')
        elif reaction.emoji == '🔁':
            await game.resend()
        else:
            return
    
    try:
        await reaction.remove(user)
    except:
        pass

@bot.command(name='start', brief='Starts a new game',help='Starts a new game in the channel the command was sent.')
async def start(ctx):
    global games, newid
    game = c4.discordgame(newid)
    newid+=1
    games.append(game)
    game.board = await ctx.send(game.getboard())
    for x in range(1,8):
        await game.board.add_reaction(f'{x}\uFE0F\u20E3')
    await game.board.add_reaction('\u23F9\uFE0F')
    await game.board.add_reaction('\U0001F501')

async def stopgame(game):
    await game.clear()

async def resend(game):
    await game.resend()

@bot.command(name='animoji', brief='Sends an animated emoji',help='Sends an animated emoji that flashes between a red and yellow piece.')
async def animoji(ctx):
    await ctx.send('<a:yred:787220892853731348>')

@bot.command(name='getgame', brief='Gets a played game',help='Retrieves and sends a previously played game by the gameid. If no gameid is given, the last ended game is retrieved.')
async def getgame(ctx, *args):
    f = open('games.txt')
    try:
        getid = int(args[0])
    except:
        getid = len(f.readlines())-1
        f.seek(0)
    for line in f.readlines():
        for i in range(len(line)):
            if line[i]==' ':
                if int(line[0:i]) == getid:
                    await ctx.send(line)
                    f.close()
                    return
                else:
                    break
    await ctx.send('no game found')
    f.close()

@bot.command(name='replay', brief='Replays a game (WIP)',help='Replays a game through a board by the gameid. If no gameid is given, the last ended game is replayed. (WIP)')
async def replay(ctx, *args):
    pass

bot.run(TOKEN)
