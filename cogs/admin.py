import discord
from discord import member
from discord.ext import commands

class AdminCommands(commands.Cog):
	def __init__(self, client):
		self.client = client

	
	#Mute
	@commands.command()
	@commands.has_permissions( administrator = True )
	async def мут(self, ctx, member: discord.Member, *, reason='По приколу'):
		
		guild = ctx.guild
		for role in guild.roles:
			if role.name == 'Muted':

				await member.add_roles(role)
				embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
				embed.set_author(name = 'Выдан мут!')
				embed.set_thumbnail(url = 'https://icon-icons.com/icons2/1290/PNG/512/2369366-emoticon-face-mute-smiley_85428.png')
				embed.set_footer(text = f'Администратор: {ctx.author}', icon_url = ctx.author.avatar_url)
				embed.add_field(name = 'Пользователь: ', value = member)
				embed.add_field(name = 'Причина: ', value = reason)
				await ctx.send(embed = embed)

	# Unmute
	@commands.command(aliases = ['анмут', 'unmute'])
	@commands.has_permissions( administrator = True )
	async def размут(self, ctx, member: discord.Member, *, reason='По приколу'):

		author = ctx.message.author
		guild = ctx.guild

		for role in guild.roles:
			if role.name == 'Muted':
				await member.remove_roles(role)
				
				embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
				embed.set_author(name = 'Выдан размут!')
				embed.set_thumbnail(url = 'https://cdn.icon-icons.com/icons2/1617/PNG/512/3700480-microphone-radio-recording-sound-technology-vintage-voice_108745.png')
				embed.set_footer(text = f'Администратор: {ctx.author}', icon_url = ctx.author.avatar_url)
				embed.add_field(name = 'Пользователь: ', value = member)
				embed.add_field(name = 'Причина: ', value = reason)
				await ctx.send(embed = embed)

	# Clear
	@commands.command(aliases = ['удалить', 'клир', 'clear'])
	@commands.has_permissions( administrator = True )
	async def очистка(self, ctx, amount = 1000000):	
		await ctx.channel.purge( limit = amount )

	# Give Role
	@commands.command()
	@commands.has_permissions(administrator = True)
	async def роль(self, ctx, member: discord.Member = None, role: discord.Role = None):

	    try:

	        if member is None:

	            await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

	        elif role is None:

	            await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: роль!**'))

	        else:

	            await discord.Member.add_roles(member, role)
	            await ctx.send(embed = discord.Embed(description = f'**Роль успешна выдана!**'))

	    except:
	        
	        await ctx.send(embed = discord.Embed(description = f'**:exclamation: Не удалось выдать роль.**', color=0x0c0c0c))

def setup(client):
	client.add_cog(AdminCommands(client))
