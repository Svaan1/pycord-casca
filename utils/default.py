import json
import os


class Config():
    def __init__(self):
        self.config = self.startup()
        self.bot_config = self.config["discord_bot"]
        self.database = self.config["database"]

    def startup(self):
        return json.load(open('config.json'))

    def get_cogs(self):
        result = []

        def add_file(file):
            if file.endswith(".py"):
                extension = f"cogs.{cog}.{file[:-3]}"
                result.append(extension)

        for cog in set(self.bot_config["cogs"]):
            for file in os.listdir(f"./cogs/{cog}"):
                add_file(file)
            for file in os.listdir("./cogs/"):
                add_file(file)
        return result
