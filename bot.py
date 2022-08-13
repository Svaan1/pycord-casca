from discord import Bot
from utils.default import Config

config = Config().bot_config


class MyBot(Bot):
    def __init__(self):
        super().__init__()
        self.startup()

    def startup(self):
        for cog in config["cogs"]:
            print(self.load_extension(f"cogs.{cog}"))


bot = MyBot()
bot.run(config["token"])
