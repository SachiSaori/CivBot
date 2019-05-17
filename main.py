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
start = False


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
            emb = discord.Embed(title="Регистрация!", color=0x00ff00)
            emb.add_field(name="Имя:", value=ctx.message.author.name, inline=True)
            emb.set_footer(text="Спасибо за участие")
        else:
            emb = discord.Embed(title="Ошибка!", color=0xff0000)
            emb.add_field(name="Имя:", value=ctx.message.author.name, inline=True)
            emb.set_footer(text="Простите, но вы уже в игре. :(")
        await ctx.send(embed=emb)

'''
@Bot.command(pass_context=True)
async def autoban(ctx):
    if ctx.channel.id == 577856202352885790:

        part.remove('Венеция')
        part.remove('Гунны')
        part.remove('Испания')

        emb = discord.Embed(title='Венеция, Гуны и Испания были забанены!', color=0x00ff00)

        part_str = ""
        for civ in part:
            part_str += str(civ) + " "

        emb.add_field(name='Выбор из', value=part_str, inline=True)
        emb.set_footer(text='Для бана используйте команду !ban "1 нация" "2 нация" (без кавычек)')
        await ctx.send(embed=emb)
'''


@Bot.command(pass_context=True)
async def ban(ctx, civ1, civ2):
    if ctx.channel.id == 577856202352885790:
        if ctx.message.author in partban:
            if (civ1.capitalize() in part) and (civ2.capitalize() in part):
                part.remove(civ1.capitalize())
                part.remove(civ2.capitalize())
                partban.remove(ctx.message.author)
                emb = discord.Embed(title='Бан!', color=0x00ffff)
                emb.add_field(name="Название", value=civ1+' '+civ2, inline=False)
                emb.set_footer(text='Данные цивилизации была забанены. Вы можете забанить максимум 2 нации!')
            else:
                emb = discord.Embed(title='Ошибка!', color=0xff0000)
                emb.add_field(name='Ошибка значений', value=ctx.message.content+' не в списке')
                emb.set_footer(text='Одной из нации нету в списке. Попробуйте ещё раз!')
        else:
            emb = discord.Embed(title='Ошибка!', color=0xff0000)
            emb.add_field(name='Ошибка значений', value=ctx.message.author.name + ' не в списке')
            emb.set_footer(text='Вы уже потратили свою возможность!')
        await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def random(ctx):
    if ctx.channel.id == 577856202352885790:
        global start
        if not start:
            start = True
            playersdictionary = GameAlgs.randomciv(players, part)
            emb = discord.Embed(title='', color=0x00ff00)
            for player in playersdictionary.keys():
                civ_str = ""
                for civ in playersdictionary[player]:
                    civ_str += civ + " "
                emb.add_field(name=player, value=civ_str, inline=True)
                civ_str = ""
            emb.set_footer(text='Старт успешен. После игры введите !clear для очистки сессии')
            await ctx.send(embed=emb)
        else:
            await ctx.send('Пожалуйста, запустите !clear')


@Bot.command(pass_context=True)
async def clear(ctx):
    players.clear()
    playerslog.clear()  # для корректной работы
    global civils
    civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон',
              'Византия', 'Германия', 'Голландия', 'Греция', 'Дания', 'Египет', 'Зулусы', 'Индия',
              'Индонезия', 'Инки','Ирокезы', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя',
              'Марокко', 'Монголия', 'Персия', 'Полинезия', 'Польша', 'Португалия', 'Рим', 'Россия', 'Сиам',
              'Сонгай', 'Турция', 'Франция', 'Швеция', 'Шошоны', 'Эфиопия', 'Япония', ]
    part.clear()
    part.extend(civils)
    partban.clear()
    global start
    start = False
    await ctx.send('Очистка прошла успешно')


@Bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Commands', color=0x00ffff)
    emb.add_field(name='!help', value='Выводит список команд бота!', inline=False)
    emb.add_field(name='!reg', value='Регистрирует участника!', inline=False)
    emb.add_field(name='!ban "Нация 1" "Нация 2"', value='Исключает две нации из выборки (без запятой, через пробел)', inline=False)
    emb.add_field(name='!random', value='Случайным образом выбирает каждому участнику три нации', inline=False)
    emb.add_field(name='!clear', value='Очищает рандомайзер. Обязательно выполнять после каждого применения бота (или перед каждым)', inline=False)
    emb.set_footer(text='Уже исключены Гунны, Венеция, Испания. \n Спасибо, что воспользовались нашим ботом! :3')
    await ctx.send(embed=emb)

Bot.run("NTc2NDA3NjA2ODU2MjUzNDQw.XNcf-w.jUeX-gFLqX_6UrVlw0r_2-J_LoQ")