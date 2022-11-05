import discord, random
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://sn1ch:E0pVjmZtYQIZylu3@cluster0.oslxn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
collusers = cluster.wgbot.users


class Experience(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        xpPerMessage = random.randint(3, 7)
        xpPerLongMessage = random.randint(7, 15)
        mainchatChannel = self.client.get_channel(723542931641860136)
        floodChannel = self.client.get_channel(723543041901592577)
        referallsChannel = self.client.get_channel(944705615857598484)
        teamsearhChannel = self.client.get_channel(707900707977560094)
        privateChannel = self.client.get_channel(723543271195803669)
        xpChannels = [mainchatChannel, floodChannel, referallsChannel, privateChannel]
        firstBoostRole = discord.utils.get(message.guild.roles, id=952539598100267038)
        secondBoostRole = discord.utils.get(message.guild.roles, id=952539707986825226)
        warnRole = discord.utils.get(message.guild.roles, id=946963344374513734)
        if message.channel in xpChannels and not warnRole in message.author.roles and not message.author.bot and not message.content.startswith(',') and not message.content.startswith(';'):
            if collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_lvl'] >= 5 and collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_lvl'] < 20:
                collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                    '$set': {
                        'user_xp_multiply': 1.3
                    }
                })
            elif collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_lvl'] >= 20:
                collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                    '$set': {
                        'user_xp_multiply': 1.5
                    }
                })
            if firstBoostRole in message.author.roles:
                if collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_lvl'] >= 5 and collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_lvl'] < 20:
                    collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                        '$set': {
                            'user_xp_multiply': 2.6
                        }
                    })

                elif collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_lvl'] >= 20:
                    collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                        '$set': {
                            'user_xp_multiply':3
                        }
                    })
                else:
                    collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                        '$set': {
                            'user_xp_multiply': 2
                        }
                    })
            elif secondBoostRole in message.author.roles:
                if collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_lvl'] >= 5 and collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_lvl'] < 20:
                    collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                        '$set': {
                            'user_xp_multiply': 3.9
                        }
                    })

                elif collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_lvl'] >= 20:
                    collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                        '$set': {
                            'user_xp_multiply': 4.5
                        }
                    })
                else:
                    collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                        '$set': {
                            'user_xp_multiply': 3
                        }
                    })
            if len(message.content) >= 47:
                collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                    '$inc': {
                        'user_xp': xpPerLongMessage*int(collusers.find_one({'user_id': message.user.id, 'user_guild_id': message.guild.id})['user_xp_multiply'])
                    }
                })
            else:
                collusers.update_one({'user_id': message.author.id, 'user_guild_id': message.guild.id}, {
                    '$inc': {
                        'user_xp': xpPerMessage*int(collusers.find_one({'user_id': message.author.id, 'user_guild_id': message.guild.id})['user_xp_multiply'])
                    }
                })

    #@commands.Cog.listener()
    #async def on_message(self, message):


    @commands.command()
    async def seexp(self, ctx):
        user_xp = collusers.find_one({'user_id': ctx.author.id, 'user_guild_id': ctx.guild.id})['user_xp']
        user_multiply = collusers.find_one({'user_id': ctx.author.id, 'user_guild_id': ctx.guild.id})['user_xp_multiply']
        await ctx.reply(f'{ctx.author}, your xp is `{user_xp}` points.\nYour multiply is `{user_multiply}`', mention_author=False)

    @commands.command()
    async def setxp(self, ctx, xp = 10, member: discord.Member = None):
        if ctx.author.id == 300626407900446721:
            if member == None:
                member = ctx.author
            if not xp < 10:
                oldXp = collusers.find_one({'user_id': member.id, 'user_guild_id': ctx.guild.id})['user_xp']
                collusers.update_one({'user_id': member.id, 'user_guild_id': ctx.guild.id}, {
                    '$set': {
                        'user_xp': xp
                    }
                })

def setup(client):
    client.add_cog(Experience(client))