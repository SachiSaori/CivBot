import discord
from discord.ext import commands
from discord.ext.commands import Bot
import GameAlgs
import settings
import Mongocon


Bot = commands.Bot(command_prefix='!')
Bot.remove_command('help')


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name='Введите !help для вывода помощи по боту'))
    print("Bot is online!")


@Bot.command(pass_context=True)
async def ban(ctx, match_id, civ1, civ2):
    user = Mongocon.User(ctx.message.author.id, ctx.message.author.name, ctx.message.author.avatar)
    match = Mongocon.Match(match_id)
    if (civ1.capitalize() in settings.part) and (
            civ2.capitalize() in settings.part):
        if ctx.message.author.name not in settings.players:
            db_ans = Mongocon.join(user, match, match_id)
            if db_ans == "В игре!":
                emb = discord.Embed(title="Ошибка!", color=0xff0000)
                emb.add_field(
                    name="Имя:",
                    value=ctx.message.author.name,
                    inline=True)
                emb.set_footer(text="Простите, но вы уже в игре или ваш хост не предоставил статистику")
            else:
                if db_ans == "Матч уже идёт!":
                    emb = discord.Embed(title="Ошибка!", color=0xff0000)
                    emb.add_field(
                        name="id:",
                        value=match_id,
                        inline=True)
                    emb.set_footer(text="Матч с этим id уже начат.")
                else:
                    settings.players.append(ctx.message.author.name)
                    settings.users_id.append(ctx.message.author.id)
                    settings.part.remove(civ1.capitalize())
                    settings.part.remove(civ2.capitalize())
                    emb = discord.Embed(
                        title=ctx.message.author.name +
                        ', Добро пожаловать в игру! ' +
                        civ1.capitalize() +
                        ' ' +
                        civ2.capitalize() +
                        ' Исключены из выборки',
                        color=0x00ffff)
                    settings.banned.append(civ1)
                    settings.banned.append(civ2)
                    banned_str = ""
                    for ban in settings.banned:
                        banned_str += ban + " "
                    emb.set_footer(
                        text='Уже забанены: ' +
                        banned_str.capitalize())
        else:
            emb = discord.Embed(title="Ошибка!", color=0xff0000)
            emb.add_field(
                name="Имя:",
                value=ctx.message.author.name,
                inline=True)
            emb.set_footer(text="Простите, но вы уже в игре. :(")
    else:
        emb = discord.Embed(title='Ошибка!', color=0xff0000)
        emb.add_field(name=civ1 + " " + civ2, value='Какой-то из этих наций нет в списке')
        emb.set_footer(text=' ')
    await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def random(ctx, match_id):
    playersdictionary = GameAlgs.randomciv()
    emb = discord.Embed(title='Старт', color=0x00ff00)
    match = Mongocon.Match(match_id)
    host, avg_point = match.start(int(match_id))
    for player in playersdictionary.keys():
        civ_str = ""
        for civ in playersdictionary[player]:
            civ_str += civ + " "
        emb.add_field(name=player, value=civ_str, inline=True)
        civ_str = ""
    emb.set_footer(
        text=f'Старт успешен. Средний рейтинг участников равен {avg_point}, хостом игры является {host}. ХОСТ ОБЯЗАН ПРЕДОСТАВИТЬ СТАТИСТИКУ ПОСЛЕ ИГРЫ!')
    settings.players.clear()
    settings.civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон',
              'Византия', 'Германия', 'Голландия', 'Греция', 'Дания', 'Египет', 'Зулусы', 'Индия',
              'Индонезия', 'Инки', 'Ирокезы', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя',
              'Марокко', 'Монголия', 'Персия', 'Полинезия', 'Польша', 'Португалия', 'Рим',
              'Россия', 'Сиам', 'Сонгай', 'Турция', 'Франция', 'Швеция', 'Шошоны', 'Эфиопия',
              'Япония']
    settings.part.clear()
    settings.part.extend(settings.civils)
    settings.partban.clear()
    settings.banned.clear()
    await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def remake(ctx, match_id):
    match = Mongocon.Match(match_id)
    user = Mongocon.User(ctx.message.author.id, ctx.message.author.name, ctx.message.author.avatar)
    ans = match.remake(user, match_id)
    if ans:
        settings.players.clear()
        settings.civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон',
                'Византия', 'Германия', 'Голландия', 'Греция', 'Дания', 'Египет', 'Зулусы', 'Индия',
                'Индонезия', 'Инки', 'Ирокезы', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя',
                'Марокко', 'Монголия', 'Персия', 'Полинезия', 'Польша', 'Португалия', 'Рим',
                'Россия', 'Сиам', 'Сонгай', 'Турция', 'Франция', 'Швеция', 'Шошоны', 'Эфиопия',
                'Япония']
        settings.part.clear()
        settings.part.extend(settings.civils)
        settings.partban.clear()
        settings.banned.clear()
        emb = discord.Embed(title='Пересоздание', color=0x00ff00)
        emb.set_footer(text="Вы можете заново создать матч!")
    else:
        emb = discord.Embed(title='Пересоздание', color=0xff0000)
        emb.set_footer(text="Вы не хост этого матча или он не существует!")
    await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def result(ctx, match_id, *args):
    mention_list: List[Any] = []
    match = Mongocon.Match(match_id)
    for mention in ctx.message.mentions:
        mention_list.append(mention.id)
    user = Mongocon.User(ctx.message.author.id, ctx.message.author.name, ctx.message.author.avatar)
    ans = match.result(user, int(match_id), mention_list)
    if ans:
        await ctx.send("Статистика обновлена!")
    else:
        await ctx.send("Вы не хост!")

@Bot.command(pss_context=True)
async def stat(ctx, mention=None):
    if len(ctx.message.mentions) == 0:
        user = Mongocon.User(ctx.message.author.id, ctx.message.author.name, ctx.message.author.avatar)
    else:
        mention = ctx.message.mentions[0]
        user = Mongocon.User(mention.id, mention.name, mention.avatar)
    statistic = user.statistic()
    emb = discord.Embed(title=statistic["name"], color=0x00ff00)
    emb.add_field(name = 'Всего игр: ', value=statistic["matches"], inline=False)
    emb.add_field(name = 'Из них побед: ', value=statistic["wins"], inline=True)
    emb.add_field(name = 'Из них поражений: ', value=statistic["loses"], inline=True)
    emb.add_field(name = 'Из них "выживаний": ', value=statistic["survives"], inline=True)
    emb.add_field(name = 'Ваш рейтинг: ', value=statistic["points"], inline=False)
    await ctx.send(embed=emb)
 

@Bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Commands', color=0x00ffff)
    emb.add_field(
        name='!ban id Нация1 Нация2',
        value='Банит две цивилизации и регистрирует вас в игру.',
        inline=False)
    emb.add_field(
        name='!random id',
        value='Выдаёт три рандомные нации!',
        inline=False)
    emb.add_field(
        name='!result id Победитель Проигравшие(Может отсутствовать!)',
        value='Обновляет рейтинг всех игроков, участвовавших в матче. Доступна только хосту!',
        inline=False,
    )
    emb.add_field(
        name='!remake id',
        value='Пересоздаёт игру с данным id. Доступна только хосту!',
        inline=False,
    )
    emb.add_field(
        name='!stat игрок(упоминанием)',
        value='Выводит статистику УПОМЯНУТОГО игрока. Если упоминания не было - выводит вашу статистику.',
        inline=False
    )
    emb.set_footer(text='')
    await ctx.send(embed=emb)

Bot.run(settings.BOT_TOKEN)
