import discord
from discord.ext import commands
from discord.ext.commands import Bot
import GameAlgs
import settings


Bot = commands.Bot(command_prefix='!')
Bot.remove_command('help')


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name='Введите !help для вывода помощи по боту'))
    print("Bot is online!")


@Bot.command(pass_context=True)
async def ban(ctx, civ1, civ2):
    if ctx.channel.id == 577856202352885790:
        if (civ1.capitalize() in settings.part) and (civ2.capitalize() in settings.part):
            if ctx.message.author.name not in settings.players:
                settings.players.append(ctx.message.author.name)
                settings.part.remove(civ1.capitalize())
                settings.part.remove(civ2.capitalize())
                emb = discord.Embed(title=ctx.message.author.name+', добро пожаловать в игру! '+civ1.capitalize()+' '+civ2.capitalize()+' Исключены из выборки', color=0x00ffff)
                settings.banned.append(civ1)
                settings.banned.append(civ2)
                banned_str = ""
                for ban in settings.banned:
                    banned_str += ban + " "
                emb.set_footer(text='Уже забанены: ' + banned_str.capitalize())
            else:
                emb = discord.Embed(title="Ошибка!", color=0xff0000)
                emb.add_field(name="Имя:", value=ctx.message.author.name, inline=True)
                emb.set_footer(text="Простите, но вы уже в игре. :(")
        else:
            emb = discord.Embed(title='Ошибка!', color=0xff0000)
            emb.add_field(name=civ1+" "+civ2, value='Этих наций нет в списке')
            emb.set_footer(text=' ')
        await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def random(ctx):
    if ctx.channel.id == 577856202352885790:
        playersdictionary = GameAlgs.randomciv(settings.players, settings.part)
        emb = discord.Embed(title='', color=0x00ff00)
        for player in playersdictionary.keys():
            civ_str = ""
            for civ in playersdictionary[player]:
                civ_str += civ + " "
            emb.add_field(name=player, value=civ_str, inline=True)
            civ_str = ""
        emb.set_footer(text='Старт успешен.')
        settings.players.clear()
        settings.civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия',
                           'Ацтеки', 'Бразилия', 'Вавилон',
                           'Византия', 'Германия', 'Голландия', 'Греция',
                           'Дания', 'Египет', 'Зулусы', 'Индия', 'Индонезия',
                           'Инки', 'Ирокезы', 'Карфаген', 'Кельты', 'Китай',
                           'Корея', 'Майя', 'Марокко', 'Монголия', 'Персия',
                           'Полинезия', 'Польша', 'Португалия', 'Рим',
                           'Россия', 'Сиам', 'Сонгай', 'Турция', 'Франция',
                           'Швеция', 'Шошоны', 'Эфиопия', 'Япония']
        settings.part.clear()
        settings.part.extend(settings.civils)
        settings.partban.clear()
        settings.banned.clear()
        await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def help(ctx):
    if ctx.channel.id == 577856202352885790:
        emb = discord.Embed(title='Commands', color=0x00ffff)
        emb.add_field(name='!ban Нация1 Нация2', value='Регистрирует участника и банит две нации из выборки.', inline=False)
        emb.add_field(name='!random', value='Случайным образом выбирает каждому участнику три нации', inline=False)
        emb.set_footer(text='Уже исключены Гунны, Венеция, Испания.')
        await ctx.send(embed=emb)

Bot.run("NTc2NDA3NjA2ODU2MjUzNDQw.XNcf-w.jUeX-gFLqX_6UrVlw0r_2-J_LoQ")
