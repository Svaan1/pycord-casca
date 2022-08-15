from discord import Bot, Intents
from utils.default import Config

config = Config().bot_config


class MyBot(Bot):
    def __init__(self):
        intents = Intents().all()
        super().__init__(intents=intents)
        self.startup()

    def startup(self):
        for cog in Config().get_cogs():
            print(self.load_extension(cog))


bot = MyBot()
bot.run(config["token"])
