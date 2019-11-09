import discord
from discord.ext import commands
from discord.ext.commands import Bot
import GameAlgs
import settings
import MySQLDB


Bot = commands.Bot(command_prefix='!')
Bot.remove_command('help')


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name='Введите !help для вывода помощи по боту'))
    print("Bot is online!")


@Bot.command(pass_context=True)
async def auth(ctx):
    DB_status = MySQLDB.add_user(ctx.message.author.name, ctx.message.author.id)
    if DB_status:
        await ctx.send("Спасибо за регистрацию! Теперь вы можете пользоваться ботом")
    else:
        await ctx.send("Вы уже есть в базе данных!")


@Bot.command(pass_context=True)
async def ban(ctx, match_id, civ1, civ2):
    if (civ1.capitalize() in settings.part) and (civ2.capitalize() in settings.part):
        if ctx.message.author.name not in settings.players:
            in_db, in_game, match_status = MySQLDB.registration(ctx.message.author.id, match_id, civ1, civ2)
            if in_db:
                if in_game:
                    if match_status:
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
                        emb.set_footer(text="Регистрация на этот матч закрыта!")
                else:
                    emb = discord.Embed(title="Ошибка!", color=0xff0000)
                    emb.add_field(name="Имя:", value=ctx.message.author.name, inline=True)
                    emb.set_footer(text="Вы уже в игре. Завершите её (Или, если игра ещё не началась, выйдите) перед тем, как зарегистрироваться в новую!")
            else:
                emb = discord.Embed(title="Ошибка!", color=0xff0000)
                emb.add_field(name="Имя:", value=ctx.message.author.name, inline=True)
                emb.set_footer(text="Вас нет в Базе Данных! Пропишите !auth перед тем, как воспользоваться ботом!")
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
async def leave(ctx):
    in_db, in_game, match_status = MySQLDB.leave(ctx.message.author.id)
    if in_db:
        if in_game:
            if match_status:
                for player in enumerate(settings.players):
                    if player[1] == ctx.message.author.name:
                        leaved_player = settings.players.pop(player[0])
                        civ1, civ2 = MySQLDB.unbanned(ctx.message.author.id)
                        settings.banned.remove(civ1)
                        settings.banned.remove(civ2)
                        settings.part.append(civ1)
                        settings.part.append(civ2)
                ans = "Вы успешно покинули матч!"
            else:
                ans = "Матч уже начался, вы не можете его покинуть!"
        else:
            ans = "Вы не находитесь в игре"
    else:
        ans = "Вас нет в базе данных"
    await ctx.send(ans)


@Bot.command(pass_context=True)
async def random(ctx):
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
    emb = discord.Embed(title='Commands', color=0x00ffff)
    emb.add_field(name='!ban Нация1 Нация2', value='Регистрирует участника и банит две нации из выборки.', inline=False)
    emb.add_field(name='!random', value='Случайным образом выбирает каждому участнику три нации', inline=False)
    emb.set_footer(text='Уже исключены Гунны, Венеция, Испания.')
    await ctx.send(embed=emb)

Bot.run("NjQyNDQ0MzY4NTgxNzU0ODgw.XcXA_g.ZNXC5FA_gnIemTYOxytMPSKTF5k")
