import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

import c4

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='c!')

games=[]

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
            await reaction.message.channel.send(f'Game: {game.game}')
        elif game.checkwin(c4.yellow):
            await reaction.message.channel.send(f"yellow ({game.p2.name}) wins!")
            await stopgame(game)
            await reaction.message.channel.send(f'Game: {game.game}')
        elif game.checkdraw():
            await reaction.message.channel.send("the game has drawn!")
            await stopgame(game)
            await reaction.message.channel.send(f'Game: {game.game}')
    
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

@bot.command(name='start')
async def start(ctx):
    global games
    game = c4.discordgame(len(games))
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

@bot.command(name='animoji')
async def animoji(ctx):
    print(ctx.message.guild.emojis)
    await ctx.send('<a:yred:787220892853731348>')
    
bot.run(TOKEN)
