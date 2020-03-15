import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re

bot = commands.Bot(command_prefix='>', description="this is a helper bot")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def suma(ctx, numOne: int, numTwo: int):
    await ctx.send(numOne+numTwo)


@bot.command()
async def test(ctx, *args):
    # '{}arguments: {}'.format(len(args),
    await ctx.send(','.join(args))
    # user = client.get_user(381870129706958858)
    # await user.send('👀')
    # await message.author.send('👋')


@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", color=discord.Color.blue())
    embed.add_field(name="Server Time", value=datetime.datetime.utcnow())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    # embed.set_thumbnail(url=f"{ctx.guild.icon}")
    url = f"{ctx.guild.icon}"
    print(url)

    await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx, *, search):
    query_String = parse.urlencode({'search_querry': search})
    html_content = request.urlopen('http://www.youtube.com/results?'+query_String)
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', html_content.read().decode())
    # print(search_results)
    await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Depresion Postparto"))
    print('MyBot isready')


async def my_message(message): pass

bot.add_listener(my_message, 'on_message')

bot.run('Njg4MjkyNTUxMjExNzQ1Mjgw.XmyMng.YgBBTTOUI-TxryRj-j5e5xzwyq4')
# https://discordapp.com/developers/applications/688292551211745280/oauth2s
# pipenv install discord.py
# pipenv shell
