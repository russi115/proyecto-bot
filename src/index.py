import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re
import os
#from boto.s3.connection import S3Connection
 


bot = commands.Bot(command_prefix='$', description="this is a helper bot")


@bot.command()
async def invite(ctx):
    """
    Muestra el link de invitación del bot.
    """
    embed = discord.Embed(title=f"", color=0xff9214)
    embed.add_field(name="**Invitación**", value=f"[Haz click aquí para obtener el enlace.](<{discord.utils.oauth_url(bot.user.id)}>)")
    embed.set_footer(text=f"{bot.user.name} fue creado por Chivito y es la nueva versión de Noulo.")
    await ctx.send(f"{ctx.author.mention}", embed=embed)

@bot.command()
async def ping(ctx):
    """
    Muestra el ping del bot
    """
    await ctx.send(f'**Pong! In {round(bot.latency * 1000)} ms**')

@bot.command()
async def hug(ctx, user: discord.Member = None):
    """
    Mandas un abrazo a otra persona.
    """

    if user is not None:
        embed = discord.Embed(title=f"", description='Abrazito', color=discord.Color.purple())
        embed.add_field(name="Nombre de usuario", value=f"{user.name}")
        embed.add_field(name="Fue abrazadó por", value=f"`{ctx.author}`")
        await ctx.send(embed=embed)

"""
@bot.command()
async def turun(ctx, channel: discord.VoiceChannel = None ):
    if channel is not None:
        await channel.connect( timeout=60.0, reconnect=True ,cls=<class'discord.voice_client.VoiceClient'>)
"""
@bot.command()
async def tururun(ctx):
    """
    Te desconecta si estas en un Voice Channel.
    """
    await ctx.author.move_to(None)
    print(ctx.author, "leave the vc")
    return await ctx.send("See You later!")


@bot.command()
async def suma(ctx, numOne: int, numTwo: int):
    """
    Realiza un suma sencilla
    """
    await ctx.send(numOne+numTwo)


@bot.command()
async def test(ctx, *, args):
    await ctx.send(args)
    await ctx.message.delete()


@bot.command()
async def info(ctx):
    """
    Muestra la informacion del server
    """
    created = ctx.guild.created_at
    created = created.strftime("%x")
    time = datetime.datetime.utcnow()
    hour = time.strftime("%X")

    embed = discord.Embed(title=f"{ctx.guild.name}", color=discord.Color.blue())
    embed.add_field(name="Server Time", value=f"{hour}")
    embed.add_field(name="Server created at", value=f"{created}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=ctx.guild.icon_url)
    url = f"{ctx.guild.icon}"
    print(url)

    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Depresion Postparto"))
    print('MyBot isready')


async def my_message(message): pass

bot.add_listener(my_message, 'busy_message')

bot.run(os.getenv("TOKEN"))
#bot.run(S3Connection(os.environ['TOKEN']))


# https://discordapp.com/developers/applications/688292551211745280/oauth2s
# pipenv install discord.py
# pipenv shell
# python src/index.py
