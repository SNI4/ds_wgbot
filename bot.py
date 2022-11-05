import discord, os, random, asyncio, win10toast
from discord.ext import commands, tasks



intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = ',', intents=intents)



TOKEN = ('NzE1MTMzNjg0MTg0Nzc2NzA0.Xs4yJA.ysE_I-rq07GhMzZHfnS4kbqjNws')
GUILD = ('𝐖𝐀𝐍𝐓𝐈𝐀𝐆𝐎𝐎 𝐇𝐎𝐔𝐒𝐄')




@client.event
async def on_ready():

	toaster = win10toast.ToastNotifier()
	toaster.show_toast('WANTIAGOO MAIN BOT', 'is connected')

	guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

	print(
		f'{client.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})'
		)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument ):
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, пользователь не найден!**', color=0x0c0c0c))


initial_extensions = []

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		initial_extensions.append(f'cogs.{filename[:-3]}')

print(initial_extensions)
if __name__ == '__main__':
	for extension in initial_extensions:
		client.load_extension(extension)


client.run(TOKEN)