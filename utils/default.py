import json

class Config():
    def __init__(self):
        self.config = self.startup()
        self.bot_config = self.config["discord_bot"]
        self.database = self.config["database"]

    def startup(self):
        return json.load(open('config.json'))
