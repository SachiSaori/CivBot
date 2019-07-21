import discord
from discord.ext import commands
from discord.ext.commands import Bot
import GameAlgs

Bot = commands.Bot(command_prefix='!')
Bot.remove_command('help')

players = []
playerslog = []  # для корректной работы
civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон', 'Византия',
          'Германия', 'Голландия', 'Греция', 'Дания', 'Египет', 'Зулусы', 'Индия', 'Индонезия', 'Инки',
          'Ирокезы', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя', 'Марокко', 'Монголия', 'Персия',
          'Полинезия', 'Польша', 'Португалия', 'Рим', 'Россия', 'Сиам', 'Сонгай', 'Турция', 'Франция', 'Швеция',
          'Шошоны', 'Эфиопия', 'Япония', ]
part = []
part.extend(civils)
partban = []
banned = []

@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name='Введите !help для вывода помощи по боту'))
    print("Bot is online!")


@Bot.command(pass_context=True)
async def reg(ctx):
    if ctx.channel.id == 577856202352885790:
        if ctx.message.author not in playerslog:
            players.append(ctx.message.author.name)
            playerslog.append(ctx.message.author)  # playerlog здесь чисто для того, чтобы всё работало корректно
            partban.extend(playerslog*2)
            emb = discord.Embed(title=ctx.message.author.name+' Зарегистрирован', color=0x00ff00)
            emb.set_footer(text=" ")
        else:
            emb = discord.Embed(title="Ошибка!", color=0xff0000)
            emb.add_field(name="Имя:", value=ctx.message.author.name, inline=True)
            emb.set_footer(text="Простите, но вы уже в игре. :(")
        await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def ban(ctx, civ1, civ2):
    if ctx.channel.id == 577856202352885790:
        if ctx.message.author in partban:
            if (civ1.capitalize() in part) and (civ2.capitalize() in part):
                part.remove(civ1.capitalize())
                part.remove(civ2.capitalize())
                partban.remove(ctx.message.author)
                emb = discord.Embed(title=civ1+' '+civ2+' Исключены из выборки', color=0x00ffff)
                banned.append(civ1)
                banned.append(civ2)
                banned_str = ""
                for ban in banned:
                    banned_str += ban + " "
                emb.set_footer(text='Уже забанены:' + banned_str,)
            else:
                emb = discord.Embed(title='Ошибка!', color=0xff0000)
                emb.add_field(name=civ1+" "+civ2, value="Уже забанены")
                banned_str = ""
                for ban in banned:
                    banned_str += ban + " "
                emb.set_footer(text='Уже забанены: ' + banned_str)
        else:
            emb = discord.Embed(title='Ошибка!', color=0xff0000)
            emb.add_field(name=ctx.message.author.name, value='Вы уже банили')
            emb.set_footer(text=' ')
        await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def random(ctx):
    if ctx.channel.id == 577856202352885790:
        playersdictionary = GameAlgs.randomciv(players, part)
        emb = discord.Embed(title='', color=0x00ff00)
        for player in playersdictionary.keys():
            civ_str = ""
            for civ in playersdictionary[player]:
                civ_str += civ + " "
            emb.add_field(name=player, value=civ_str, inline=True)
            civ_str = ""
        emb.set_footer(text='Старт успешен.')
        players.clear()
        playerslog.clear()  # для корректной работы
        global civils
        civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон',
                  'Византия', 'Германия', 'Голландия', 'Греция', 'Дания', 'Египет', 'Зулусы', 'Индия',
                  'Индонезия', 'Инки','Ирокезы', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя',
                  'Марокко', 'Монголия', 'Персия', 'Полинезия', 'Польша', 'Португалия', 'Рим', 'Россия', 'Сиам',
                  'Сонгай', 'Турция', 'Франция', 'Швеция', 'Шошоны', 'Эфиопия', 'Япония']
        part.clear()
        part.extend(civils)
        partban.clear()
        banned.clear()
        await ctx.send(embed=emb)

@Bot.command(pass_context=True)
async def help(ctx):
    if ctx.channel.id == 577856202352885790:
        emb = discord.Embed(title='Commands', color=0x00ffff)
        emb.add_field(name='!reg', value='Регистрирует участника.', inline=False)
        emb.add_field(name='!ban Нация 1 Нация 2', value='Исключает две нации из выборки (без запятой, через пробел)', inline=False)
        emb.add_field(name='!random', value='Случайным образом выбирает каждому участнику три нации', inline=False)
        emb.set_footer(text='Уже исключены Гунны, Венеция, Испания.')
        await ctx.send(embed=emb)

Bot.run("NTc2NDA3NjA2ODU2MjUzNDQw.XNcf-w.jUeX-gFLqX_6UrVlw0r_2-J_LoQ")