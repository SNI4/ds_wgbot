import discord, minestat, asyncio, requests, datetime
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord.utils import get


class VCupdate(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.gameactivityServerStatus.start()

    # self.streamerInfo.start()

    # Custom Voice Create
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel.id == 944066410081054770:
            for guild in self.client.guilds:
                if guild.id == 707866473342959666:
                    mainCategory = discord.utils.get(guild.categories, id=944066620127608844)
                    channel2 = await guild.create_voice_channel(name=f"{member.display_name}", category=mainCategory)
                    await member.move_to(channel2)
                    await channel2.set_permissions(member, manage_channels=True)

                    def check(a, b, c):
                        return len(channel2.members) == 0

                    await self.client.wait_for('voice_state_update', check=check)
                    await channel2.delete()

    # Server Status
    @tasks.loop()
    async def gameactivityServerStatus(self):
        workChannel = self.client.get_channel(944585248547680286)
        onlineChannel = self.client.get_channel(944585327199281202)
        pingChannel = self.client.get_channel(944585351035490364)
        timeChannel = self.client.get_channel(946936846976434227)

        while True:

            ms = minestat.MineStat('wgcraft.ru', 25565)
            msServerStatus = 'OFFLINE'
            timeNow = datetime.datetime.now()
            timeNowEdited = timeNow.strftime('%H:%M:%S')

            if ms.online:
                msServerStatus = 'ONLINE'
                await workChannel.edit(name=f'🟩STATUS: {msServerStatus}🟩')
                await onlineChannel.edit(name=f'🧑PLAYERS: {ms.current_players}/{ms.max_players}🧑')
                await pingChannel.edit(name=f'🔄PING: {int(ms.latency)}🔄')
                await timeChannel.edit(name=f'🕜EDIT: {timeNowEdited}🕦')

            else:
                msServerStatus = 'OFFLINE'
                await workChannel.edit(name=f'🔴STATUS: {msServerStatus}🔴')
                await onlineChannel.edit(name='🆘STARTUP-WAIT🆘')
                await pingChannel.edit(name='🆘STARTUP-WAIT🆘')
                await timeChannel.edit(name=f'EDIT AT {timeNowEdited}')

            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f',help | made by sn1ch#1337'))
            await asyncio.sleep(300)

    @gameactivityServerStatus.before_loop
    async def before_gameactivityServerStatus(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(VCupdate(client))


'''		
    	@tasks.loop()
				async def streamerInfo(self):
					twitchStats = 'https://www.twitchmetrics.net/c/572281489-wantiagoo'
					twitchSbStats = 'https://www.twitch.tv/wantiagoo'
					headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

					streamerInfoChannel = self.client.get_channel(945121212944764958)
					streamerLastSeenChannel = self.client.get_channel(945141736764756018)
					allFollowerChannel = self.client.get_channel(945504127029485578)
					rankChannel = self.client.get_channel(945509639888465980)

					while True:

						followersStat = requests.get(twitchStats, headers=headers)
						twitchSbStatsr = requests.get(twitchSbStats, headers=headers)

						if followersStat.status_code == 200:
							followersStatPage = BeautifulSoup(followersStat.text, 'html.parser')
							twitchSbStatsPagerPage = BeautifulSoup(twitchSbStatsr.text, 'html.parser')

							try:

								findLastSeen = followersStatPage.find('time', class_='time_ago')
								findLastSeenOrig = findLastSeen.text
								findLastSeenName = findLastSeenOrig.replace(' ', '', 3)
								await streamerLastSeenChannel.edit(name=f'📜 LAST: {(findLastSeenName)[4:]} 📜')
							except:
								await streamerLastSeenChannel.edit(name='⚫ troubles with web-site.. ⚫')


							liveFollowerCount = twitchSbStatsPagerPage.find('p', style='CoreText-sc-cpl358-0 jKJSbc')
							rankPlace = followersStatPage.find('strong')

							await rankChannel.edit(name=f'🏆 RANK: {rankPlace.text} 🏆')
							await allFollowerChannel.edit(name=f'💜 FOLLOWERS: {liveFollowerCount.text} 💜')
						else:
							await allFollowerChannel.edit(name=f'⚫ troubles with web-site.. ⚫')

						await asyncio.sleep(5)

	@streamerInfo.before_loop
	async def before_streamerInfo(self):
		await self.client.wait_until_ready()
'''