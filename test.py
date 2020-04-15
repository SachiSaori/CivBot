import discord
from discord.ext import commands
from discord.ext.commands import Bot

Bot = commands.Bot(command_prefix='!')
Bot.remove_command('help')


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name='Введите !help для вывода помощи по боту'))
    print("Bot is online!")

@Bot.command(pass_context=True)
async def t(ctx, *args):
    mention_list=[]
    for mention in ctx.message.mentions:
        mention_list.append(mention.id)
    await ctx.send(mention_list)

Bot.run("NjQyNDQ0MzY4NTgxNzU0ODgw.XnUBGQ.P73HOVqOVpPUVawFK5stmg80ghs")
