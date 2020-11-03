import discord
from discord.ext import commands
from urllib import parse, request
import requests as rq
import idna_ssl

bot = commands.Bot(command_prefix='$', description="this is a helper bot")

class Goodreads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("goodreads is ready")

    @bot.command()
    async def Books(self, ctx, *, q):
        try: 
            end = 'https://v1.nocodeapi.com/russi115/gr/pIEwcCNhuMxpIImD/search'
            url = end + '?q=' + q
            print(url)
            r = rq.get(url=url).json()
            print(r)
            await ctx.send('help me')
        except Exception as error:
            print(error)
            


    @bot.command()
    #@commands.cooldown(rate=1, per=5, type=command.BucketType.default)
    async def Mybooks(self, ctx, *, uid):
        try: 
            # https://www.goodreads.com/user/show/19311570-jenny
            uid = uid.split('/')#array
            uid = uid[-1]#19311570-jenny
            name = uid.split('-')
            name = name[-1]
            channel = ctx.channel

            end = "https://v1.nocodeapi.com/russi115/gr/pIEwcCNhuMxpIImD/myBooks"
            url = end + '?uid=' + uid
            r = rq.get(url=url).json()
            array = r["books"]
            embed = discord.Embed(title=f"{'Goodreads- Books of the user '+ name}", color=discord.Color.blue(), description=f"{name+' have '+str(r['total'])+ ' books in total!'}\n\n")
            embed.description +=""
            for x in range(int(r["total"]/2)):
                title= array[x]["book"]["title"]
                embed.description += "• "+f"{title}\n"
            embed.description+="\nPage 1/2| Use the emotes to switch pages\n"
            msg_embed = await ctx.send(embed=embed)
            await msg_embed.add_reaction("◀️")
            await msg_embed.add_reaction("▶️")

            c=0
            while c<5:
                try:
                    self.descp = "**\nReacciona a este mensaje para ver el resto de la lista."
                    def check(reaction, user):
                        return (str(reaction.emoji) == "▶️" or str(reaction.emoji) == "◀️") and user.id == ctx.author.id 
                    
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)

                    if str(reaction) == "▶️":
                        y=10
                        embed = discord.Embed(title=f"{'Goodreads- Books of the user '+ name}", color=discord.Color.blue(), description=f"{name+' have '+str(r['total'])+ ' books in total!'}\n\n")                   
                        for z in range(int(r["total"]/2)):
                            title = array[y]["book"]["title"]                        
                            embed.description += "• "+f"{title}\n"
                            y+=1
                        embed.description+="\nPage 2/2| Use the emotes to switch pages\n"
                        await msg_embed.edit(embed=embed)
                        

                    elif str(reaction) == "◀️":
                        embed = discord.Embed(title=f"{'Goodreads- Books of the user '+ name}", color=discord.Color.blue(), description=f"{name+' have '+str(r['total'])+ ' books in total!'}\n\n")                   
                        for n in range(int(r["total"]/2)):
                            title = array[n]["book"]["title"]                        
                            embed.description += "• "+f"{title}\n"
                        embed.description+="\nPage 1/2| Use the emotes to switch pages\n"
                        await msg_embed.edit(embed=embed)
                        
                    try:
                        await msg_embed.remove_reaction(reaction, user)
                        c+=1
                    
                    except Exception:
                        self.descp = f"**\nError removing reactions**."
                
                except Exception as error:
                    print(error)
            
            try:
                await msg_embed.remove_reaction(reaction, user)   
                await msg_embed.remove_reaction(str("▶️"), ctx.guild.me) 
                await msg_embed.remove_reaction(str("◀️"), ctx.guild.me)                
            except Exception:
                self.descp = f"**\nError removing reactions**."
           

        except Exception as error:
                print("error;",error)


def setup(bot):
    bot.add_cog(Goodreads(bot))            