import discord
from discord.ext import commands
from utils.default import Config

config = Config().bot_config


class MyBot(discord.Bot):
    def __init__(self):
        super().__init__(debug_guilds=[
            1002615670749536326, 596410699496947712])
        self.startup()

    def startup(self):
        for cog in config["cogs"]:
            try:
                self.load_extension(f"cogs.{cog}")
                print(f"{cog} loaded")
            except Exception as why:
                print(f"Failed to load {cog}")
                print(why)


bot = MyBot()
bot.run(config["token"])
