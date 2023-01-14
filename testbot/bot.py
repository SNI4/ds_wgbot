import discord, asyncio, win10toast
from pymongo import MongoClient
from discord.ext import commands
from itertools import cycle

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=';', intents=intents)

cluster = MongoClient('mongodb+srv://sn1ch:E0pVjmZtYQIZylu3@cluster0.oslxn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
collusers = cluster.wgbot.users

@client.event
async def on_ready():
	toaster = win10toast.ToastNotifier()
	toaster.show_toast('WANTIAGOO TEST BOT', 'is connected')
	xp = collusers.find_one({'username': 'sn1ch'})['user_xp']
	print(xp)
	print('bot connected')

@client.event
async def on_message(message):
	if not message.author.bot:
		channel = client.get_channel(723543041901592577)
		if message.content.startswith('l'):
			await channel.send('fsd')
		else:
			await channel.send('lol')

@client.command()
async def animtest(ctx):
	animation = ['|', '/', '-', '\\', '|', '/', '-', '\\']
	mes = await ctx.send('anim')
	while True:
		for item in cycle(animation):
			await mes.edit(content=item)
			await asyncio.sleep(0.5)

@client.command()
async def ping(ctx):
	mes = await ctx.send('tracking...')
	await asyncio.sleep(0.8)
	await mes.edit(content=f'i think latency is {round(client.latency*1000)} ms')

client.run('')
