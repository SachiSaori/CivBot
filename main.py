# -*- coding: cp1251 -*-

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import GameAlgs
import settings


Bot = commands.Bot(command_prefix='!')
Bot.remove_command('help')


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name='������� !help ��� ������ ������ �� ����'))
    print("Bot is online!")


@Bot.command(pass_context=True)
async def ban(ctx, civ1, civ2):
    if (civ1.capitalize() in settings.part) and (
            civ2.capitalize() in settings.part):
        if ctx.message.author.name not in settings.players:
            settings.players.append(ctx.message.author.name)
            settings.users_id.append(ctx.message.author.id)
            settings.part.remove(civ1.capitalize())
            settings.part.remove(civ2.capitalize())
            emb = discord.Embed(
                title=ctx.message.author.name +
                ', ����� ���������� � ����! ' +
                civ1.capitalize() +
                ' ' +
                civ2.capitalize() +
                ' ��������� �� �������',
                color=0x00ffff)
            settings.banned.append(civ1)
            settings.banned.append(civ2)
            banned_str = ""
            for ban in settings.banned:
                banned_str += ban + " "
            emb.set_footer(
                text='��� ��������: ' +
                banned_str.capitalize())
        else:
            emb = discord.Embed(title="������!", color=0xff0000)
            emb.add_field(
                name="���:",
                value=ctx.message.author.name,
                inline=True)
            emb.set_footer(text="��������, �� �� ��� � ����. :(")
    else:
        emb = discord.Embed(title='������!', color=0xff0000)
        emb.add_field(name=civ1 + " " + civ2, value='���� ����� ��� � ������')
        emb.set_footer(text=' ')
    await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def random(ctx):
    playersdictionary = GameAlgs.randomciv(settings.players, settings.part)
    emb = discord.Embed(title='�����', color=0x00ff00)
    for player in playersdictionary.keys():
        civ_str = ""
        for civ in playersdictionary[player]:
            civ_str += civ + " "
        emb.add_field(name=player, value=civ_str, inline=True)
        civ_str = ""
    emb.set_footer(
        text=f'����� �������.')
    settings.players.clear()
    settings.civils = ['�������', '�������', '������', '������', '�������',
                       '������', '��������', '�������',
                       '��������', '��������', '���������', '������',
                       '�����', '������', '������', '�����', '���������',
                       '����', '�������', '��������', '������', '�����',
                       '�����', '����', '�������', '��������', '������',
                       '���������', '������', '����������', '���',
                       '������', '����', '������', '������', '�������',
                       '������', '������', '�������', '������']
    settings.part.clear()
    settings.part.extend(settings.civils)
    settings.partban.clear()
    settings.banned.clear()
    await ctx.send(embed=emb)


@Bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Commands', color=0x00ffff)
    emb.add_field(
        name='!ban �����1 �����2',
        value='������������ ��������� � ����� ��� ����� �� �������.',
        inline=False)
    emb.add_field(
        name='!random',
        value='��������� ������� �������� ������� ��������� ��� �����',
        inline=False)
    emb.set_footer(text='��� ��������� �����, �������, �������.')
    await ctx.send(embed=emb)

Bot.run("NTc2NDA3NjA2ODU2MjUzNDQw.Xg9E2g.mwyRVMohKYvixtE7mdUgfiDaRTc")
