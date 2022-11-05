import discord, os
from discord.ext import commands, tasks
from pymongo import MongoClient

cluster = MongoClient(
    'mongodb+srv://sn1ch:E0pVjmZtYQIZylu3@cluster0.oslxn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
collusers = cluster.wgbot.users
collservers = cluster.wgbot.servers


class WarnSystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='warn')
    @commands.has_permissions(administrator=True)
    async def give_warn(self, ctx, member: discord.Member, *, reason='No reason.'):
        role = discord.utils.get(ctx.guild.roles, id=946963344374513734)
        floodChannel = self.client.get_channel(723543041901592577)
        if member is None:
            await ctx.reply('You must specify the user.', mention_author=None)
        if member.bot is True:
            await ctx.reply('You can\'t warn `bot`!', mention_author=False)
        elif collusers.find_one({'_id': member.id, 'user_guild_id': ctx.guild.id})['user_warns'] >= 4:
            collusers.update_one({'_id': member.id, 'user_guild_id': ctx.guild.id}, {
                 '$set': {
                      'user_warns': 0
                 }
            })
            await member.remove_roles(role)
            await floodChannel.send(f'`{member.name}` received 5th warn and has been removed from guild.')
        else:
            collusers.update_one({'_id': member.id, 'user_guild_id': ctx.guild.id}, {
                '$inc': {
                     'user_warns': 1
                },
                '$push': {
                    'user_warns_list': {
                        'admin_id': ctx.author.id,
                        'warn_reason': reason
                    }
                }
            })
            await member.add_roles(role)
            totalWarns = str(collusers.find_one({'_id': member.id, 'user_guild_id': ctx.guild.id})['user_warns'])
            await ctx.reply(f'{ctx.author} has warned `{member}`. Total warns: `{totalWarns}`', mention_author=False)


    @commands.command(name='rewarn')
    @commands.has_permissions(administrator=True)
    async def remove_warn(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, id=946963344374513734)
        if member is None:
            await ctx.reply('You must specify the user.', mention_author=False)
        elif collusers.count_documents({'_id': member.id, 'user_guild_id': ctx.guild.id}) == 0:
            await ctx.reply(f'{member.name} has no warns.', mention_author=False)
        else:
            collusers.update_one({'_id': member.id, 'user_guild_id': ctx.guild.id}, {
                '$inc': {
                    'user_warns': -1
                }
            })
            totalWarns = str(collusers.find_one({'_id': member.id, 'user_guild_id': ctx.guild.id})['user_warns'])
            await ctx.reply(f'{member.mention} has unwarned. `{totalWarns}` more warning(s) left.', mention_author=False)


def setup(client):
    client.add_cog(WarnSystem(client))
