import discord
from discord.ext import commands

from utils.sql_handler import Database

class Economy_Database(Database):
    # Dummy functions to be added
    def get_money_value_from_id():
        pass
    def update_money_value_from_id():
        pass
    def register_new_account():
        pass

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Economy_Database("Economy")

    @commands.command()
    async def teste(self, ctx):
        await ctx.send(self.database.table_name)
    
    #Dummy functions to be added
    def give_money():
        pass
    def check_currency():
        pass

def setup(bot):
    bot.add_cog(Economy(bot))
