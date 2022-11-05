import discord, random, asyncio
from discord.ext import commands

class Games(commands.Cog):
	def __init__(self, client):
		self.client = client

	# Stone, Scissors, Paper!
	@commands.command()
	async def кнб( self, ctx, arg ):
		author = ctx.message.author
		choice = random.randint(1,3)
		
		if choice == 1:
			compChoice = 'камень'
		elif choice == 2:
			compChoice = 'ножницы'
		else:
			compChoice = 'бумага'
		await ctx.send( f'{author.mention}, Ваш выбор: {arg}, Выбор Бота: {compChoice}!' )
		if arg == compChoice:
			await ctx.send( f'Ничья!' )
		elif arg == 'камень' and compChoice == 'ножницы':
			await ctx.send( f'Победил игрок!' )

		elif arg == 'камень' and compChoice == 'бумага' :
			await ctx.send( f'Победил Бот!' )

		elif arg == 'ножницы' and compChoice == 'бумага':
			await ctx.send( f'Победил игрок!' )

		elif arg == 'ножницы' and compChoice == 'камень':
			await ctx.send( f'Победил Бот!' )

		elif arg == 'бумага' and compChoice == 'камень' :
			await ctx.send( f'Победил игрок!' )

		elif arg == 'бумага' and compChoice == 'ножницы':
			await ctx.send( f'Победил Бот' )

		else:
			await ctx.send( f'Вы долбаеб.' )

	# Dice
	@commands.command()
	async def кости(self, ctx, member: discord.Member):
		check1 = lambda message: message.author == ctx.author and message.channel == ctx.channel
		check2 = lambda message: message.author == member and message.channel == ctx.channel
		timeEmbed=discord.Embed(colour=15158332, title='Время вышло!')
		timeEmbed.set_author(name='Игра отменена.')
		timeEmbed.set_thumbnail(url='https://cdn-icons.flaticon.com/png/512/6061/premium/6061782.png?token=exp=1646136527~hmac=7e54203c728b8352fbb9d82384496086')
		embed=discord.Embed(colour=15844367, title='Ожидаем второго игрока...')
		#embed.set_image(url='https://media.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif')
		embed.set_author(name='КОСТИ')
		embed.set_thumbnail(url='https://cdn-icons-png.flaticon.com/512/1479/1479689.png')
		embed.add_field(name='Первый игрок:', value=f'`{ctx.message.author}`')
		embed.add_field(name='Второй игрок:', value=f'`{member}`')
		embed.add_field(name='Подсказка:', value='`,принять`', inline=False)
		message1 = await ctx.reply(embed=embed, mention_author=False)
		#message1 = await ctx.send(f'Вы отправили запрос на игру в кости участнику {member}, ожидаем его решения...\nНапишите `,принять` чтобы начать игру!')
		await member.send(f'Участник сервера {ctx.guild.name} с ником {ctx.author} отправил вам запрос на игру в кости **в канале <#{ctx.channel.id}>**.\nПерейдите в канал и напишите `,принять`, чтобы принять вызов!')
		await message1.add_reaction('<a:timer60:947245198994460743>')
		try:
			acceptMessage = await self.client.wait_for('message', check=check2, timeout = 60)
		except asyncio.TimeoutError:
			await ctx.send(embed=timeEmbed)
			await message1.delete()
			await acceptMessage.delete()
		while acceptMessage.content != ',принять':
			acceptMessage = await self.client.wait_for('message', check=check2, timeout = 60)
		if acceptMessage.content == ',принять':
			await message1.delete()
			await acceptMessage.delete()
			message2 = await ctx.send(f'Второй игрок принял запрос! Первым бросает кости участник {ctx.message.author.mention} (`,бросить`)')
			await message2.add_reaction('<a:timer60:947245198994460743>')
			try:
				dice1Message = await self.client.wait_for('message', check=check1, timeout = 60)
			except asyncio.TimeoutError:
				await ctx.send(embed=timeEmbed)
				await dice1Message.delete()
				await message2.delete()
			while dice1Message.content != ',бросить':
				dice1Message = await self.client.wait_for('message', check=check1, timeout = 60)
			if ',бросить' in dice1Message.content:
				await message2.delete()
				await dice1Message.delete()
				dice1 = random.randint(1, 7)
				embed=discord.Embed(colour=15844367, title=f'Результат первого броска {ctx.message.author}')
				embed.set_image(url='https://media.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif')
				embed.set_author(name='КОСТИ')
				embed.add_field(name='Первая кость:', value=f'`{dice1}`')
				embed.add_field(name='Вторая кость:', value='`Ожидание...`')
				embed.add_field(name='Игрок:', value=f'`{ctx.message.author}`', inline=False)
				embed.add_field(name='Подсказка:', value='`,бросить`', inline=False)
				message3 = await ctx.reply(embed=embed, mention_author=False)
				#message3 = await ctx.send(f'{ctx.message.author} бросил первую кость! Результат: **{dice1}**. Ожидаем второй бросок... (`,бросить`)')
				await message3.add_reaction('<a:timer60:947245198994460743>')
				try:
					dice2Message = await self.client.wait_for('message', check=check1, timeout = 60)
				except asyncio.TimeoutError:
					await ctx.send(embed=timeEmbed)
					await message3.delete()
					await dice2Message.delete()
				while dice2Message.content != ',бросить':
					dice2Message = await self.client.wait_for('message', check=check1, timeout = 60)

				if ',бросить' in dice2Message.content:
					await message3.delete()
					await dice2Message.delete()
					dice2 = random.randint(1, 7)
					authorAllDice = dice1 + dice2
					embed=discord.Embed(colour=15844367, title=f'Результат игрока {ctx.message.author}')
					embed.set_image(url='https://media.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif')
					embed.set_author(name='КОСТИ')
					embed.add_field(name='Первая кость:', value=f'`{dice1}`')
					embed.add_field(name='Вторая кость:', value=f'`{dice2}`')
					embed.add_field(name='Общий результат:', value=f'`{authorAllDice}`')
					embed.add_field(name='Игрок:', value=f'`{ctx.message.author}`', inline=False)
					embed.add_field(name=f'Ожидаем броска {member} ', value='`,бросить`')
					message4 = await ctx.reply(embed=embed, mention_author=False)
					#message4 = await ctx.send(f'{ctx.message.author} бросил вторую кость! Результат: **{dice2}**.\nОбщий результат двух бросков: **{authorAllDice}**\nОжидаем бросок игрока {member.mention}. (`,бросить`)')
					await message4.add_reaction('<a:timer60:947245198994460743>')
					try:
						dice3Message = await self.client.wait_for('message', check=check2, timeout = 60)
					except asyncio.TimeoutError:
						await ctx.send(embed=timeEmbed)
						await message4.delete()
						await dice3Message.delete()
					while dice3Message.content != ',бросить':
						dice3Message = await self.client.wait_for('message', check=check2, timeout = 60)

					if ',бросить' in dice3Message.content:
						await message4.delete()
						await dice3Message.delete()
						dice3 = random.randint(1, 7)
						embed=discord.Embed(colour=15844367, title=f'Результат первого броска {member}')
						embed.set_image(url='https://media.giphy.com/media/ckHAdLU2OmY7knUClD/giphy.gif')
						embed.set_author(name='КОСТИ')
						embed.add_field(name='Первая кость:', value=f'`{dice3}`')
						embed.add_field(name='Вторая кость:', value=f'`Ожидание...`')			
						embed.add_field(name='Игрок:', value=f'`{member}`', inline=False)
						embed.add_field(name='Подсказка:', value='`,бросить`')
						message5 = await ctx.reply(embed=embed, mention_author=False)
						#message5 = await ctx.send(f'{member} бросил первую кость! Результат: **{dice3}**. Ожидаем второй бросок... (`,бросить`)')
						await message5.add_reaction('<a:timer60:947245198994460743>')
						try:
							dice4Message = await self.client.wait_for('message', check=check2, timeout = 60)
						except asyncio.TimeoutError:
							await ctx.send(embed=timeEmbed)
							await message5.delete()
							await dice4Message.delete()
						while dice4Message.content != ',бросить':
							dice4Message = await self.client.wait_for('message', check=check2, timeout = 60)
						if dice4Message.content == ',бросить':
							await message5.delete()
							await dice4Message.delete()
							dice4 = random.randint(1, 7)
							memberAllDice = dice3 + dice4
							await ctx.reply(f'{member} бросил вторую кость! Результат: **{dice4}**.\nОбщий результат двух бросков: **{memberAllDice}**', mention_author=False)
						if authorAllDice > memberAllDice:
							await ctx.send(f'Победил игрок {ctx.message.author.mention}, с общим результатом **{authorAllDice}**!')
						elif authorAllDice == memberAllDice:
							await ctx.send(f'Ничья! Общий результат первого игрока: **{authorAllDice}**, а второго: **{memberAllDice}**')
						else:
							await ctx.send(f'Победил игрок {member.mention}, с общим результатом **{memberAllDice}**!')


def setup(client):
	client.add_cog(Games(client))