import discord
import GameAlgs

civils = ['Австрия', 'Америка', 'Англия', 'Аравия', 'Ассирия', 'Ацтеки', 'Бразилия', 'Вавилон', 'Венеция', 'Византия',
          'Германия', 'Голландия', 'Греция', 'Гунны', 'Дания', 'Египет', 'Зулусы', 'Индия', 'Индонезия', 'Инки',
          'Ирокезы', 'Испания', 'Карфаген', 'Кельты', 'Китай', 'Корея', 'Майя', 'Марокко', 'Монголия', 'Персия',
          'Полинезия', 'Польша', 'Португалия', 'Рим', 'Россия', 'Сиам', 'Сонгай', 'Турция', 'Франция', 'Швеция',
          'Шошоны', 'Эфиопия', 'Япония', ]
start = False
civ = ""
banned = []

client = discord.Client()


@client.event
async def on_ready():
    print('Bot is ready')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    players = []
    playerslog = []

    if message.content.startswith("!c рег"):
        if message.author in playerslog:
            await message.channel.send(f'Вы уже участвуете в игре, {message.author}')
        else:
            if len(players) < 8:
                playerslog.append(message.author)
                players.append(message.author.name+'#'+message.author.discriminator)
                await message.channel.send(f'Игрок {message.author} был добавлен в игру')
            else:
                await message.channel.send(f'Извините,{message.author} мест больше нет')
    if message.content.startswith("!c старт"):
        part = [GameAlgs.autoban(civils)]
        await message.channel.send(f'Игра была начата. Автоматически были забанены 3 нации. У вас остались следующие:{part}, вы можете забанить нацию командой "!c бан"')
    if message.content.startswith("!c список"):
        await message.channel.send(f'В данный момент участвуют следующие игроки: {players}')


client.run("NTc2NDA3NjA2ODU2MjUzNDQw.XNWDpA.pjw8dWS6syS9ZzYp5EBPv7ATYqk")
