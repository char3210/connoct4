import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

import c4

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='c!')

p1=p2=None
nums = ['1\uFE0F\u20E3']
board = None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected')


@bot.event
async def on_reaction_add(reaction, user):
    
    if user.bot:
        return

    if (reaction.message==board)==False:
        return
    
    global p1, p2
    if p1==None:
        p1=user
        await reaction.message.channel.send(f"Player 1 has joined: {user.name} ({c4.red})")
    elif p2==None:
        p2=user
        await reaction.message.channel.send(f"Player 2 has joined: {user.name} ({c4.yellow})")

    
    try:
        chosen = int(reaction.emoji[0])-1
    except:
        return

    if (user == p1 and c4.currentPiece == c4.red) or (user==p2 and c4.currentPiece == c4.yellow):
        if not c4.place(c4.cols[chosen]):
                await reaction.message.channel.send("invalid move, next to go is still "+c4.currentPiece)
    else :
        await reaction.message.channel.send("It is not your turn!")

    
    await reaction.remove(user)
    await board.edit(content = c4.getboard())
    
    if c4.checkwin('<:red:588903539926106112>'):
        await reaction.message.channel.send(f"red ({p1.name}) wins!")
        stopgame()
    elif c4.checkwin('<:yellow:588903561149153280>'):
        await reaction.message.channel.send(f"yellow ({p2.name}) wins!")
        stopgame()
    elif c4.checkdraw():
        await reaction.message.channel.send("the game has drawn!")
        stopgame()
    

@bot.command(name='start')
async def start(ctx):
    stopgame()
    global board
    board = await ctx.send(c4.getboard())
    for x in range(1,8):
        await board.add_reaction(f'{x}\uFE0F\u20E3')

@bot.command(name='stop')
async def stopcmd(ctx):
    stopgame()
    await ctx.send('game has been stopped')

def stopgame():
    global p1, p2, board
    c4.clear()
    p1=None
    p2=None
    board = None

@bot.command(name='resend')
async def resendBoard(ctx, dontclearprev):
    global board
    if not board == None:
        if not bool(dontclearprev):
            await board.delete()
        board = await ctx.send(c4.getboard())
        for x in range(1,8):
            await board.add_reaction(f'{x}\uFE0F\u20E3')
    else:
        await ctx.send('no ongoing game rn')

@bot.command(name='animoji')
async def animoji(ctx):
    print(ctx.message.guild.emojis)
    await ctx.send('<a:yred:787220892853731348>')
    
bot.run(TOKEN)
