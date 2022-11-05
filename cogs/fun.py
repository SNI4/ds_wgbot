import discord, wikipedia, qrcode, nekos, requests, random, time, asyncio, os
from discord.ext import commands
from deep_translator import GoogleTranslator


class FunCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Ping
    @commands.command(aliases=['ping', 'пинг'])
    async def задержка(self, ctx):
        message = await ctx.reply("Понг!", mention_author=False)
        await asyncio.sleep(0.5)
        await message.edit(content=f"Понг!  `{round(self.client.latency * 1000)} ms`")


    # Wiki
    @commands.command()
    async def вики(self, ctx, *, text):
        wikipedia.set_lang("ru")
        new_page = wikipedia.page(text)
        summ = wikipedia.summary(text)
        emb = discord.Embed(
            title=new_page.title,
            description=summ
        )
        emb.set_author(name='Читать дальше', url=new_page.url,
                       icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png')

        await ctx.reply(embed=emb, mention_author=False)

    # User-Card
    @commands.command()
    async def карта(self, ctx, member: discord.Member):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]

        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

        embed.set_author(name=f"Информация пользователя - {member} ")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Запросил : {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Name", value=member.display_name)

        embed.add_field(name="Зарегистрирован ", value=member.created_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"))
        embed.add_field(name="Вошел на сервер", value=member.joined_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"))

        embed.add_field(name=f"Роли({len(roles)})", value="".join(role.mention for role in roles))
        embed.add_field(name="Высшая роль", value=member.top_role.mention)

        embed.add_field(name="Бот", value=member.bot)

        await ctx.send(embed=embed)

    # RP
    @commands.command(aliases=['трахнуть', 'отьебать', 'выебать'])
    async def секс(self, ctx, member: discord.Member):
        author = ctx.message.author
        await ctx.reply(f'{author.mention} выебал пользовтеля {member.mention} 😳', mention_author=False)

    @commands.command()
    async def отсосать(self, ctx, member: discord.Member):
        author = ctx.message.author
        await ctx.reply(f'{author.mention} отсосал пользователю {member.mention} 😏', mention_author=False)

    @commands.command()
    async def отпиздить(self, ctx, member: discord.Member):
        author = ctx.message.author
        await ctx.reply(f'{author.mention} отпиздил пользователя {member.mention} 🤕', mention_author=False)

    # QR Code
    @commands.command()
    async def куар(self, ctx, *, arg):
        value = arg
        img = qrcode.make(value)
        img.save('qrcode.png')
        with open('qrcode.png', 'rb') as gp:
            await ctx.reply(file=discord.File(gp, 'qrcode.png', mention_author=False))
        os.remove('qrcode.png')

    # Hentai
    @commands.command(aliases=['хент'])
    async def хентай(self, ctx):
        if ctx.channel.is_nsfw():

            r = ['pussy', 'hentai', 'anal', 'tits', 'kuni']
            rnek = nekos.img(random.choice(r))
            await ctx.reply(f'{rnek} {ctx.author.mention}, дрочи!', mention_author=False)
        else:

            await ctx.reply(f'{ctx.author}, попробуй в NSFW канале.', mention_author=True)

    # IP-info
    @commands.command()
    async def пробей(self, ctx, arg):
        response = requests.get(f'http://ipinfo.io/{arg}/json')

        user_ip = response.json()['ip']
        user_city = response.json()['city']
        user_region = response.json()['region']
        user_country = response.json()['country']
        user_location = response.json()['loc']
        user_org = response.json()['org']
        user_timezone = response.json()['timezone']

        global all_info
        emb = discord.Embed(title=f'Информация о айпи {arg}:',
                            description=f':united_nations: **Страна**: {user_city}\n\n:regional_indicator_r: **Регион**: {user_region}\n\n:cityscape: **Город**: {user_country}\n\n:map: **Локация**: {user_location}\n\n:bust_in_silhouette: **Организация**: {user_org}\n\n:clock: **Временная зона**: {user_timezone}',
                            colour=0x39d0d6, inline=False)
        emb.set_footer(text="Вызвано: {}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)

        await ctx.reply(embed=emb, mention_author=False)

    # Avatar
    @commands.command(name='аватар', aliases=['ава', 'фото', 'аватарка', 'avatar', 'ava'])
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f'Фото **вашего** профиля: {ctx.author.avatar_url}')
        else:
            await ctx.send(f'Фото профиля **{member}**: {member.avatar_url}')

    # Translator
    # https://pypi.org/project/deep-translator/#check-supported-languages
    @commands.command(name='перевести', aliases=['tr', 'tl', 'транс'])
    async def translate(self, ctx, lang='en', *, text):
        try:
            embed = discord.Embed(colour=15105570, title='translate')
            # embed.add_field(name='src', value=f'`{lang}`')
            embed.add_field(name='dest', value=f'`{lang}`')
            # embed.add_field(name='tr', value=f'`{ctranslator}`')
            embed.add_field(name='trs text', value=f'`{GoogleTranslator(source="auto", target=lang).translate(text)}`')
            embed.set_footer(text='func in dev')
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(colour=15158332, title='Error!')
            embed.add_field(name='error', value='wrong language or troubles with bot')
            embed.add_field(name='exc', value='try to change lang `(en)`', inline=False)
            embed.set_footer(text='func in dev')
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(FunCommands(client))
