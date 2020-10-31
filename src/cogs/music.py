from discord.ext import commands
import lavalink
from discord import utils
from discord import Embed 

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
        print('bot connected to Lavalink in port', 3000)


     
        #member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        

    @commands.command(name='play')
    async def play(self, ctx, *, query):
        member = ctx.author
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                print('join command worked')
                await self.connect_to(ctx.guild.id, str(vc.id))
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            query = f'ytsearch:{query}'
            print(query)
            results = await player.node.get_tracks(query)
            tracks = results['tracks'][0:10] 
            i = 0
            query_result = ''
            for track in tracks:
                i = i +1
                query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
            embed = Embed()
            embed.description = query_result
            await ctx.channel.send(embed=embed)

            def check(m):
                return m.author.id == ctx.author.id

            response = await self.bot.wait_for('message', check=check)
            track = tracks[int(response.content)-1]

            player.add(requester=ctx.author.id, track=track)
            if not player.is_playing:
                await player.play()

        except Exception as error:
            print(error)

    @commands.command(name='stop')
    async def stop(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if player.is_playing:
            await player.stop()

    @commands.command(name='skip')
    async def skip(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if player.is_playing:
            await player.skip()

    @commands.command(name='resume')
    async def resume(self, ctx):
         player = self.bot.music.player_manager.get(ctx.guild.id)
         if not player.is_playing:
             await player.play()

    @commands.command(name='queue')
    async def queue(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        queue = player.queue
        print(queue)
        print(queue.AudaioTrack.title)
        print(queue[0].title)
        embed = Embed()
        for i in queue:
            embed.description = player.queue.title
        await ctx.channel.send(embed=embed)
        
    @commands.command(name='np')
    async def np(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        embed = Embed()
        print(player.current)
        embed.description = player.current
        await ctx.channel.send(embed=embed)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)


def setup(bot):
    bot.add_cog(MusicCog(bot))