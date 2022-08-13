from discord import Bot
from discord.ext import commands
from utils.default import Config

config = Config().bot_config


class MyBot(Bot):
    def __init__(self):
        super().__init__()
        self.startup()

    def startup(self):
        for cog in config["cogs"]:
            try:
                self.load_extension(f"cogs.{cog}")
                print(f"{cog} loaded.")
            except Exception as why:
                print(f"Failed to load {cog}")
                print(why)


bot = MyBot()
bot.run(config["token"])
