import os
import tracemalloc
import asyncio

import discord
from dotenv import load_dotenv
from discord.ext import commands

import c4

tracemalloc.start()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='c!')

games = []
newid = -1


@bot.event
async def on_ready():
    print(f'{bot.user} has connected')
    try:
        f = open('games.txt')
    except FileNotFoundError:
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
    if game is None:
        return

    try:
        chosen = int(reaction.emoji[0]) - 1
        if not (chosen in range(0, 7)):
            return
        await game.handle(chosen, user)
    except ValueError:  # is probably jank
        if reaction.emoji == '⏹️':
            game.state = 'Game has been aborted'
            await game.board.edit(content=game.getboard())
            game.stop()  # turn this into forfeits maybe
        elif reaction.emoji == '🔁':
            await game.resend()
        else:
            return

    try:
        await reaction.remove(user)
    except discord.errors.NotFound:
        pass


@bot.command(name='start',
             brief='Starts a new game',
             help='Starts a new game in the channel the command was sent.')
async def start(ctx):
    global games, newid
    game = c4.discordgame(newid)
    newid += 1
    games.append(game)
    game.board = await ctx.send(game.get_board())
    for x in range(1, 8):
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
             help='Replays a game through a board by the gameid. '
                  'If no gameid is given, the last ended game is replayed. (WIP)',
             usage='c!getgame (gameid)')
async def replay(ctx, *args):
    f = open('games.txt')
    try:
        getid = int(args[0])
    except ValueError or IndexError:  # does this even work lmao
        getid = len(f.readlines()) - 1
        f.seek(0)
    for line in f.readlines():
        for i in range(len(line)):
            if line[i] == ' ':
                if int(line[0:i]) == getid:
                    game = c4.discordgame(getid)
                    spaces = []
                    for j in range(len(line)):
                        if line[j] == ' ':
                            spaces.append(j)
                    if len(spaces) == 3:
                        game.p1 = c4.fakeplayer(line[spaces[0] + 1:spaces[1]])
                        game.p2 = c4.fakeplayer(line[spaces[1] + 1:spaces[2]])
                        moves = line[spaces[2] + 1:len(line) - 1]

                        game.update_player()
                        game.board = await ctx.send(game.get_board())

                        for x in range(len(moves)):
                            await asyncio.sleep(2)
                            game.place(int(moves[x]))
                            await game.board.edit(content=game.get_board())
                    else:
                        await ctx.send(f'Game {getid} was aborted or corrupted')
                    f.close()
                    return

                else:
                    break
    await ctx.send('no game found')
    f.close()


bot.run(TOKEN)
