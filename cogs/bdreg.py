import discord
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://sn1ch:E0pVjmZtYQIZylu3@cluster0.oslxn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
collusers = cluster.wgbot.users
collservers = cluster.wgbot.servers

class MongoReg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            totalUsers = guild.member_count
            for member in guild.members:
                if not member.bot is True:
                    user_values = {
                        '_id': member.id,
                        'username': member.name,
                        'user_id': member.id,
                        'user_guild_name': guild.name,
                        'user_guild_id': guild.id,
                        'user_xp': 10,
                        'user_xp_multiply': 1,
                        'user_lvl': 1,
                        'user_warns': 0,
                        'user_warns_list': []
                    }
                    server_values = {
                        'guild_name': guild.name,
                        'guild_id': guild.id,
                        'guild_total_users': totalUsers
                    }

                    if collusers.count_documents({'_id': member.id, 'user_guild_id': guild.id}) == 0:
                        collusers.insert_one(user_values)
                    if collservers.count_documents({'guild_id': guild.id}) == 0:
                        collservers.insert_one(server_values)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        user_values = {
            '_id': member.id,
            'username': member.name,
            'user_id': member.id,
            'user_guild_name': member.guild.name,
            'user_guild_id': member.guild.id,
            'user_xp': 10,
            'user_xp_multiply': 1,
            'user_lvl': 1,
            'user_warns': 0,
            'user_warns_list': []
        }
        if collusers.count_documents({'_id': member.id, 'user_guild_id': member.guild.id}):
            collusers.insert_one(user_values)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        totalUsers = guild.member_count
        server_values = {
            'guild_name': guild.name,
            'guild_id': guild.id,
            'guild_total_users': totalUsers
        }
        if collservers.count_documents({'guild_id': guild.id}) == 0:
            collservers.insert_one(server_values)


def setup(client):
    client.add_cog(MongoReg(client))

