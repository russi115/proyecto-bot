from discord.ext import commands
import discord
import lavalink
from discord import utils
from discord import Embed 
import re

url_rx = re.compile(r'https?://(?:www\.)?.+')
class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node(
            "localhost",
            3000,
            'testing',
            'na',
            'music-node')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)
        lavalink.add_event_hook(self.track_hook)
        print('bot connected to Lavalink in port', 3000)



     
        #member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        
    @commands.command(aliases=['play','p'])
    async def play(self, ctx, *, query):
        try:
            member = ctx.author
            if member is not None and member.voice is not None:
                vc = member.voice.channel
                player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
                if not player.is_connected:
                    player.store('channel', ctx.channel.id)
                    await self.connect_to(ctx.guild.id, str(vc.id))
            try:
                player = self.bot.music.player_manager.get(ctx.guild.id)
                query = query.strip('<>')
                embed = Embed(color=discord.Color.blurple())
                if not url_rx.match(query):
                    query =f'ytsearch:{query}'
                    print('is not a link')
                    results = await player.node.get_tracks(query)

                    tracks = results['tracks'][0:10] 
                    i = 0
                    query_result = ''
                    for track in tracks:
                        i +=+1
                        query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
                    embed.description = query_result
                    await ctx.channel.send(embed=embed)

                    def check(m):
                        return m.author.id == ctx.author.id

                    response = await self.bot.wait_for('message', check=check)
                    track = tracks[int(response.content)-1]

                    player.add(requester=ctx.author.id, track=track)
                    embed =Embed(color=discord.Color.blurple())
                    embed.title = 'Track Enqueued'
                    embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
                    await ctx.send(embed=embed)
                    if not player.is_playing:
                        await player.play()

                if not results or not results['tracks']:
                    return await ctx.send('Nothing found!')

                if results['loadType'] == 'PLAYLIST_LOADED':
                    tracks = results['tracks'] 
                    for track in tracks:
                        player.add(requester=ctx.author.id, track=track)    
                    embed.title = 'Playlist Enqueued!'
                    embed.description = f'{results["playlistInfo"]["aliases"]} - {len(tracks)} tracks'
                    await ctx.channel.send(embed=embed)

                elif results['loadType'] == 'TRACK_LOADED':
                    track = results['tracks'][0]
                    player.add(requester=ctx.author.id, track=track)
                    embed.title = 'Track Enqueued'
                    embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
                    await ctx.channel.send(embed=embed)
                    
                if not player.is_playing:
                    await player.play()  

            except Exception as error:
                print(error)          

        except Exception as error:
            print(error)

    @commands.command(aliases=['stop','s'])
    async def stop(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if player.is_playing:
            await player.set_pause(True)

    @commands.command(aliases=['skip','sk'])
    async def skip(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if player.is_playing:
            await player.skip()
            await ctx.send('Skiped current song!')

    @commands.command(aliases=['resume','r'])
    async def resume(self, ctx):
         player = self.bot.music.player_manager.get(ctx.guild.id)
         if player.paused:
             await player.set_pause(False)

    @commands.command(aliases=['queue','q'])
    async def queue(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        queue = player.queue
        embed = Embed(color=discord.Color.blurple())
        embed.title = "Queue of tracks"
        embed.description = "Songs that will sound!\n"
        i=0
        for Audio in queue:
            embed.description += "• "+f'{queue[i]["title"]}\n'
            i+=1
        await ctx.channel.send(embed=embed)
        
    @commands.command(aliases=['np'])
    async def np(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        embed = Embed(color=discord.Color.blurple())
        embed.title = "Now Playing!"
        embed.description = f'{player.current["title"]}'
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        """ Disconnects the player from the voice channel and clears its queue. """
        player = self.bot.music.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            # We can't disconnect, if we're not connected.
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            # Abuse prevention. Users not in voice channels, or not in the same voice channel as the bot
            # may not disconnect the bot.
            return await ctx.send('You\'re not in my voicechannel!')

        # Clear the queue to ensure old tracks don't start playing
        # when someone else queues something.
        player.queue.clear()
        # Stop the current track so Lavalink consumes less resources.
        await player.stop()
        # Disconnect from the voice channel.
        await self.connect_to(ctx.guild.id, None)
        await ctx.send('* | Disconnected.')

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)


def setup(bot):
    bot.add_cog(MusicCog(bot))