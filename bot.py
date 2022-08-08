import discord
from discord.ext import commands
from utils.default import Config

config = Config().bot_config

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config["command_prefix"],
            intents=discord.Intents.all()
            )
        self.loaded_cogs = config["cogs"]
        self.startup()
    
    def startup(self):
        for cog in self.loaded_cogs:
            try:
                self.load_extension(cog)
            except Exception:
                print(f"Failed to load {cog}")

bot = MyBot()
bot.run(config["token"])
