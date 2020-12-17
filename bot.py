import os
import tracemalloc
import discord
import asyncio

from dotenv import load_dotenv
from discord.ext import commands, tasks

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
        f = open('games.txt', 'w+')
    global newid
    newid = len(f.readlines())
    f.close()

def getgame(board):
    for game in games:
        if board == game.board:
            return game
    return None

@bot.event
async def on_reaction_add(reaction, user):
    
    if user.bot:
        return
    
    game = getgame(reaction.message)
    if(game == None):
        return
    
    chosen = None
    try:
        chosen = int(reaction.emoji[0])-1
        if (not (chosen in range(0,7))):
            return
        await game.handle(chosen, user)
    except:
        if reaction.emoji == '⏹️':
            game.stop()
            await reaction.message.channel.send('game has been stopped')
        elif reaction.emoji == '🔁':
            await game.resend()
        else:
            return
    
    
    await reaction.remove(user)

@bot.command(name='start',
             brief='Starts a new game',
             help='Starts a new game in the channel the command was sent.')
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

@bot.command(name='animoji',
             brief='Sends an animated emoji',
             help='Sends an animated emoji that flashes between a red and yellow piece.')
async def animoji(ctx):
    await ctx.send('<a:yred:787220892853731348>')

@bot.command(name='replay',
             brief='Replays a game (WIP)',
             help='Replays a game through a board by the gameid. If no gameid is given, the last ended game is replayed. (WIP)',
             usage='c!getgame (gameid)')
async def replay(ctx, *args):
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
                    replay = c4.discordgame(getid)
                    spaces=[]
                    for j in range(len(line)):
                        if line[j]==' ':
                            spaces.append(j)
                    replay.p1 = line[spaces[0]+1:spaces[1]]
                    replay.p2 = line[spaces[1]+1:spaces[2]]
                    moves = line[spaces[2]+1:len(line)-1]

                    replay.board = await ctx.send(replay.getboard())
                    
                    for x in range(len(moves)):
                        await asyncio.sleep(2)
                        replay.place(int(moves[x]))
                        await replay.board.edit(content=replay.getboard())
                    f.close()
                    return
                else:
                    break
    await ctx.send('no game found')
    f.close()

bot.run(TOKEN)
