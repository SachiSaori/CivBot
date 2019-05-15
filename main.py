import discord
from discord.ext import commands
from discord.ext.commands import Bot
import GameAlgs

Bot = commands.Bot(command_prefix='!')
players = []
playerslog = []  # для корректной работы
civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон', 'Венеция', 'Византия',
          'Германия', 'Голландия', 'Греция', 'Гунны', 'Дания', 'Египет', 'Зулусы', 'Индия', 'Индонезия', 'Инки',
          'Ирокезы', 'Испания', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя', 'Марокко', 'Монголия', 'Персия',
          'Полинезия', 'Польша', 'Португалия', 'Рим', 'Россия', 'Сиам', 'Сонгай', 'Турция', 'Франция', 'Швеция',
          'Шошоны', 'Эфиопия', 'Япония', ]
part = []
part.extend(civils)
partban = []


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name='Введите !helps для вывода помощи по боту'))
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
async def start(ctx):
    if ctx.channel.id == 577856202352885790:
        playersdictionary = GameAlgs.randomciv(players, part)
        emb = discord.Embed(title='Игра началась!', color=0x00ff00)
        for player in playersdictionary.keys():
            emb.add_field(name='Игрок:', value=player, inline=False)
            for civ in playersdictionary[player]:
                emb.add_field(name='Нации:', value=civ, inline=True)
        emb.set_footer(text='Старт успешен. После игры введите !clear для очистки сессии')
        await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def clear(ctx):
    players.clear()
    playerslog.clear()  # для корректной работы
    civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон', 'Венеция',
                  'Византия',
                  'Германия', 'Голландия', 'Греция', 'Гунны', 'Дания', 'Египет', 'Зулусы', 'Индия', 'Индонезия', 'Инки',
                  'Ирокезы', 'Испания', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя', 'Марокко', 'Монголия', 'Персия',
                  'Полинезия', 'Польша', 'Португалия', 'Рим', 'Россия', 'Сиам', 'Сонгай', 'Турция', 'Франция', 'Швеция',
                  'Шошоны', 'Эфиопия', 'Япония', ]
    part.clear()
    partban.clear()
    await ctx.send('Очистка прошла успешно')


@Bot.command(pass_context=True)
async def helps(ctx):
    emb = discord.Embed(title='Commands', color=0x00ffff)
    emb.add_field(name='!helps', value='Выводит команды бота!', inline=False)
    emb.add_field(name='!reg', value='Регистрирует вас в игру!', inline=False)
    emb.add_field(name='!autoban', value='автоматический бан трёх наций!', inline=False)
    emb.add_field(name='!ban', value='Участник банит одну из наций!', inline=False)
    emb.add_field(name='!start', value='Начинает игру и выдаёт каждому из участников три нации для выбора', inline=False)
    emb.add_field(name='!clear', value='Начинает процедуру очистки сессии. ВАЖНО, ИСПОЛЬЗУЙТЕ ЕЁ ПОСЛЕ КАЖДОЙ ИГРЫ!!!!', inline=False)
    emb.set_footer(text='Спасибо за использование наших услуг! Мы вам очень рады! :3')
    await ctx.send(embed=emb)

Bot.run("NTc2NDA3NjA2ODU2MjUzNDQw.XNcf-w.jUeX-gFLqX_6UrVlw0r_2-J_LoQ")
