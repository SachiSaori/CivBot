import discord
from discord.ext import commands
from discord.ext.commands import Bot
import GameAlgs

Bot = commands.Bot(command_prefix='!civ ')
players = []
playerslog = []  # для корректной работы
civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон', 'Венеция', 'Византия',
          'Германия', 'Голландия', 'Греция', 'Гунны', 'Дания', 'Египет', 'Зулусы', 'Индия', 'Индонезия', 'Инки',
          'Ирокезы', 'Испания', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя', 'Марокко', 'Монголия', 'Персия',
          'Полинезия', 'Польша', 'Португалия', 'Рим', 'Россия', 'Сиам', 'Сонгай', 'Турция', 'Франция', 'Швеция',
          'Шошоны', 'Эфиопия', 'Япония', ]
part = []
partban = []


@Bot.event
async def on_ready():
    print("Bot is online!")


@Bot.command(pass_context=True)
async def reg(ctx):
    if ctx.message.author not in playerslog:
        players.append(ctx.message.author.name)
        playerslog.append(ctx.message.author)  # playerlog здесь чисто для того, чтобы всё работало корректно
        emb = discord.Embed(title="Registration!", color=0x00ff00)
        emb.add_field(name="Name:", value=ctx.message.author.name, inline=True)
        emb.set_footer(text="Спасибо за участие")
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title="Failure!", color=0xff0000)
        emb.add_field(name="Name:", value=ctx.message.author.name, inline=True)
        emb.set_footer(text="Простите, но вы уже в игре. :(")
        await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def close(ctx):
    part.extend(GameAlgs.autoban(civils))
    partban.extend(playerslog)
    emb = discord.Embed(title='Фаза регистрации закончена!', color=0x00ff00)
    for name in players:
        emb.add_field(name="players", value=name, inline=False)
    part_str = ""
    for civ in part:
        part_str += str(civ) + " "
    emb.add_field(name='Choice from:', value=part_str, inline=True)
    emb.set_footer(text='Для бана используйте команду !civ ban "название цивилизации" (без кавычек)')
    await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def ban(ctx, civ):
    if ctx.message.author in partban:
        if civ in part:
            part.remove(civ)
            partban.remove(ctx.message.author)
            emb = discord.Embed(title='Бан!', color=0xff0000)
            emb.add_field(name="Название", value=civ, inline=False)
            emb.set_footer(text='Данная цивилизация была забанена. Учтите, один игрок может забанить только одну нацию!')
        else:
            emb = discord.Embed(title='ERROR!', color=0xff0000)
            emb.add_field(name='ValueError', value=ctx.message.content+' not in list')
            emb.set_footer(text='Данной нации нету в списке. Попробуйте ещё раз!')
    else:
        emb = discord.Embed(title='ERROR!', color=0xff0000)
        emb.add_field(name='IndexError', value=ctx.message.author.name + ' not in list')
        emb.set_footer(text='Вы уже банили в этой партии')
    await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def start(ctx):
    playersdictionary = GameAlgs.randomciv(players, part)
    emb = discord.Embed(title='Игра началась!', color=0x00ff00)
    for player in playersdictionary.keys():
        emb.add_field(name='Name:', value=player, inline=False)
        for civ in playersdictionary[player]:
            emb.add_field(name='Civ:', value=civ, inline=True)
    emb.set_footer(text='please, after game run "!civ clear" command!')
    await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def clear(ctx):
    players = []
    playerslog = []  # для корректной работы
    civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон', 'Венеция',
              'Византия',
              'Германия', 'Голландия', 'Греция', 'Гунны', 'Дания', 'Египет', 'Зулусы', 'Индия', 'Индонезия', 'Инки',
              'Ирокезы', 'Испания', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя', 'Марокко', 'Монголия', 'Персия',
              'Полинезия', 'Польша', 'Португалия', 'Рим', 'Россия', 'Сиам', 'Сонгай', 'Турция', 'Франция', 'Швеция',
              'Шошоны', 'Эфиопия', 'Япония', ]
    part = []
    partban = []
    await ctx.send('Clear successfully')


@Bot.command(pass_context=True)
async def helps(ctx):
    emb = discord.Embed(title='Commands', color=0x00ffff)
    emb.add_field(name='!civ helps', value='Выводит команды бота!', inline=False)
    emb.add_field(name='!civ reg', value='Регистрирует вас в игру!', inline=False)
    emb.add_field(name='!civ close', value='Закрывает возможность регистрации и запускает автоматический бан трёх наций!', inline=False)
    emb.add_field(name='!civ ban', value='Участник банит одну из наций!', inline=False)
    emb.add_field(name='!civ start', value='Начинает игру и выдаёт каждому из участников три нации для выбора', inline=False)
    emb.add_field(name='!civ clear', value='Начинает процедуру очистки сессии. ВАЖНО, ИСПОЛЬЗУЙТЕ ЕЁ ПОСЛЕ КАЖДОЙ ИГРЫ!!!!', inline=False)
    emb.set_footer(text='Спасибо за использование наших услуг! Мы вам очень рады! :3')
    await ctx.send(embed=emb)


Bot.run("NTc2NDA3NjA2ODU2MjUzNDQw.XNcf-w.jUeX-gFLqX_6UrVlw0r_2-J_LoQ")
