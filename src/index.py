import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re

bot = commands.Bot(command_prefix='>', description="this is a helper bot")


@bot.command()
async def role(ctx):
    print("roles:",ctx.author.roles)
    list = ctx.author.roles[1].members
    mention = ctx.author.roles[1].mention
    await ctx.send(mention)

    print("members:\n {} \n {}".format(list[0].name,list[1].name))
    mention = list[0].mention
    await ctx.send(mention)

@bot.command()
async def invite(ctx):
    """
    Muestra el link de invitación del bot.
    """
    embed = discord.Embed(title=f"", color=0xff9214)
    embed.add_field(name="**Invitación**", value=f"[Haz click aquí para obtener el enlace.](<{discord.utils.oauth_url(bot.user.id)}>)")
    embed.set_footer(text=f"{PyBot} fue creado por Hatchens.com y es la nueva versión de Auguste.")
    await ctx.send(f"{ctx.author.mention}", embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f'**Pong! In {round(bot.latency * 1000)} ms**')


@bot.command()
@commands.is_owner()
async def reload(ctx, cog: str):
    """
    Comando con el propósito de ser utilizado solo por el desarrollador.
    """
    bot.add_cog(is_owner(bot))

    try:
        bot.unload_extension(cog)
        bot.load_extension(cog)
    except Exception as error:
        await ctx.send("> No se puso reiniciar cog, **error:**\n".format(error))


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
    await ctx.send(numOne+numTwo)


@bot.command()
async def test(ctx, *, args):
    await ctx.send(args)
    await ctx.message.delete()


@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", color=discord.Color.blue())
    embed.add_field(name="Server Time", value=datetime.datetime.utcnow())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=ctx.guild.icon_url)
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

bot.add_listener(my_message, 'busy_message')

bot.run('Njg4MjkyNTUxMjExNzQ1Mjgw.XmyMZA.PARA7nTVgjJVp2DUQAPVEpM3UoM')


# https://discordapp.com/developers/applications/688292551211745280/oauth2s
# pipenv install discord.py
# pipenv shell
# python src/index.py
