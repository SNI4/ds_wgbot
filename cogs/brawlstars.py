import discord, brawlstats, random
from pymongo import MongoClient
from discord.ext import commands, tasks

cluster = MongoClient('mongodb+srv://sn1ch:E0pVjmZtYQIZylu3@cluster0.oslxn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
collbsprofiles = cluster.wgbotwarns.collbsprofiles

bsimages = {
	'https://brawl-stars.info/wp-content/webp-express/webp-images/uploads/2021/12/Эль-Тигро.png.webp': 15844367,
	'https://brawl-stars.info/wp-content/webp-express/webp-images/uploads/2021/12/Нянь-Нита.png.webp': 1752220,
	'https://brawl-stars.info/wp-content/webp-express/webp-images/uploads/2021/11/Майк-с-плесенью.png.webp': 5763719,
	'https://brawl-stars.info/wp-content/webp-express/webp-images/uploads/2021/10/Капитан-Ворон.png.webp': 3447003,
	'https://brawl-stars.info/wp-content/webp-express/webp-images/uploads/2021/04/Молниеносный-.png.webp': 15548997
}

class BrawlStars(commands.Cog):

	def __init__(self, client):
		with open('bstoken.txt', 'r') as bstoken:
			bstok = bstoken.read()
		self.stat = brawlstats.Client(bstok, is_async=True)
		self.client = client


	@commands.command()
	async def setbsprofile(self, ctx, tag: str):
		user_value = {
			'username': ctx.author,
			'user_id': ctx.author.id,
			'guild_id': ctx.author.id,
			'bstag': tag
		}
		if collbsprofiles.count_documents({'user_id': ctx.author.id, 'guild_id': ctx.guild.id}) == 0:
			collbsprofiles.insert_one(user_value)
			await ctx.reply('Successful!\nYou can check your Brawl Stars profile with command `,bsprofile`', mention_author=False)
		else:
			await ctx.reply('This user already has brawl stars profile!', mention_author = False)


	@commands.command()
	async def delbsprofile(self, ctx, member: discord.Member = None):
		collbsprofiles.delete_one({'user_id': ctx.author.id})
		await ctx.reply(f'Operation successful, `{ctx.author}` profile `has been removed`.', mention_author=False)	

	@commands.command()
	async def lookbsprofile(self, ctx, tag):
		if tag is None:
			await ctx.reply('You need to specify user tag.', mention_author=False)
		else:
			try:
				player = await self.stat.get_profile(tag)
			except brawlstars.RequestError as e:
				await ctx.reply(f'```\n{e.code}: {e.message}\n```', mention_author=False)

			bsRandomChoice = random.choices(list(bsimages.items()))
			img = bsRandomChoice[0][0]
			color = bsRandomChoice[0][1]
			#allBrawlers = player.brawlers
			#topBrawler = allBrawlers[0]

			embed = discord.Embed(colour=color, timestamp=ctx.message.created_at)
			embed.set_image(url=img)
			embed.set_thumbnail(url='https://yt3.ggpht.com/ytc/AKedOLQBp2GxgEc-WE5RL6phbHQhfaw6UvKofBejsH1O=s900-c-k-c0x00ffffff-no-rj')
			embed.set_author(name=f'{player.name} Brawl Stars Profile')
			embed.set_footer(text=f'{player.tag}, {player.name}', icon_url = ctx.author.avatar_url)
			embed.add_field(name='🏆 Trophies `|` Highest Trophies 🏆', value=f'`{player.trophies}` | `{player.highest_trophies}`', inline=True)
			embed.add_field(name='🥇 3v3 Victories `|` Solo Victories 🥇', value=f'`{player.x3vs3_victories}` | `{player.solo_victories}`', inline=False)
			embed.add_field(name='🛡 Club Name `|` Club Tag 🛡', value=f'`{player.club.name}` | `{player.club.tag}`', inline=False)
			#embed.add_field(name='🎖 Top Brawler (bug) 🎖', value=f'`{topBrawler.name}` | Trophies: `{topBrawler.trophies}` | Power: `{topBrawler.power}` | Rank: `{topBrawler.rank}`', inline=False)
			embed.add_field(name='📊 Experience Level `|` Experience Points 📊', value=f'`{player.exp_level}` | `{player.exp_points}`', inline=False)
			await ctx.reply(embed=embed, mention_author=False)

	@commands.command()
	async def bsprofile(self, ctx, member: discord.Member = None):
		if member is None:
			member = ctx.author
		bsRandomChoice = random.choices(list(bsimages.items()))
		img = bsRandomChoice[0][0]
		color = bsRandomChoice[0][1]
		usr = collbsprofiles.find_one({'user_id': member.id, 'guild_id': ctx.guild.id})
		tag = usr['bstag']
		player = await self.stat.get_profile(tag)
		allBrawlers = player.brawlers
		topBrawler = allBrawlers[0]
		embed = discord.Embed(colour=color, timestamp=ctx.message.created_at)
		embed.set_image(url=img)
		embed.set_thumbnail(url='https://yt3.ggpht.com/ytc/AKedOLQBp2GxgEc-WE5RL6phbHQhfaw6UvKofBejsH1O=s900-c-k-c0x00ffffff-no-rj')
		embed.set_author(name=f'{member} Brawl Stars Profile')
		embed.set_footer(text=f'{player.tag}, {player.name}', icon_url=member.avatar_url)
		embed.add_field(name='🏆 Trophies `|` Highest Trophies 🏆', value=f'`{player.trophies}` | `{player.highest_trophies}`', inline=True)
		embed.add_field(name='🥇 3v3 Victories `|` Solo Victories 🥇', value=f'`{player.x3vs3_victories}` | `{player.solo_victories}`', inline=False)
		embed.add_field(name='🛡 Club Name `|` Club Tag 🛡', value=f'`{player.club.name}` | `{player.club.tag}`', inline=False)
		#embed.add_field(name='🎖 Top Brawler (bug) 🎖', value=f'`{topBrawler.name}` | Trophies: `{topBrawler.trophies}` | Power: `{topBrawler.power}` | Rank: `{topBrawler.rank}`', inline=False)
		embed.add_field(name='📊 Experience Level `|` Experience Points 📊', value=f'`{player.exp_level}` | `{player.exp_points}`', inline=False)
		await ctx.reply(embed=embed, mention_author=False)

	@commands.command()
	async def clubprofile(self, ctx, tag: str):
		try:
			clan = await self.stat.get_club(tag)
		except brawlstats.RequestError as e:
			await ctx.reply(f'```\n{e.code}: {e.message}\n```', mention_author=False)
		page1=discord.Embed(colour=2123412, timestamp=ctx.message.created_at)
		page1.set_image(url='https://blog.brawlstars.com/uploaded-images/1015649975_1623263772.jpg?mtime=20210609183611')
		page1.set_thumbnail(url='https://cspromogame.ru//storage/upload_images/avatars/4527.jpg')
		page1.set_author(name=f'{clan.name} stats:')
		page1.add_field(name='Club Name `|` Club Tag', value=f'`{clan.name}` | `{clan.tag}`')
		page1.add_field(name='Trophies `|` Required Trophies', value=f'`{clan.trophies}` | `{clan.required_trophies}`', inline=False)
		page1.add_field(name='Club Type', value=f'`{clan.type}`', inline=False)
		await ctx.reply(embed=page1, mention_author=False)

		'''
		page2=discord.Embed(colour=11027200, title=f'Members count: {len(clanMembers)}')
		x=0
		while not x == len(clan.members):
			page2.add_field(
				name=f'{x+1}. `{clan.members[x].name}`',
				value=f'Tag: `{clan.members[x].tag}`. Trophies: `{clan.members[x].trophies}`.',
				inline=False
				)
			x += 1

		page3=discord.Embed(colour=11027200, title=f'Members count: {len(clanMembers)}')
		y=9
		while not y == len(clan.members):
			page3.add_field(
				name=f'{y+1}. `{clan.members[y].name}`',
				value=f'Tag: `{clan.members[y].tag}`. Trophies: `{clan.members[y].trophies}`.',
				inline=False
				)
			y += 1

		page4=discord.Embed(colour=11027200, title=f'Members count: {len(clanMembers)}')
		z=19
		while not z == len(clan.members):
			page4.add_field(
				name=f'{z+1}. `{clan.members[z].name}`',
				value=f'Tag: `{clan.members[z].tag}`. Trophies: `{clan.members[z].trophies}`.',
				inline=False
				)
			z += 1

		components=[
			ActionRow([
					Button(
							label='↩',
							style=ButtonType().Primary,
							custom_id='left_button'
						),
					Button(
							label='↪',
							style=ButtonType().Primary,
							custom_id='right_button'
						)
				])
		]

	
		await buttons.send(embed=page1, components=components)

	@buttons.click
	async def right_button(self, ctx):
		await ctx.reply('test', mention_author=False)
	'''

	@commands.command()
	async def clubmembers(self, ctx, tag: str):
		clan = await self.stat.get_club(tag)
		clanMembers = clan.members
		embed=discord.Embed(colour=11027200, title=f'Members count: {len(clanMembers)}')
		x=0
		while not x == len(clanMembers):
			embed.add_field(
				name=f'{x+1}. `{clanMembers[x].name}`',
				value=f'Tag: `{clanMembers[x].tag}`. Trophies: `{clanMembers[x].trophies}`.',
				inline=False
				)
			x += 1
		await ctx.reply(embed=embed, mention_author=False)

def setup(client):
	client.add_cog(BrawlStars(client))