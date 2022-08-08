# discordpy-bot

A simple discord bot made with discordpy which, at the moment, does the following:

- You can set the channels which the bot "listens to" by storing the channel id in the **channels_to_listen** variable, there's probably a better way to do this but im unfamiliar with this api and the guild system

- When mentioned the bot will reply with a specific message (plan on doing a random message from a list)

- The bot will react with an emoji (right now :rofl:) to every message from people on people_to_annoy

- And it has also an anonymous message system, which every message (or image) DM'ed to the bot will be sent anonymously to the channel in main_channel_id, for now it only works in one channel and i plan to change that and make a way to choose the desired server when doing this

To-Do

1. Make the variable information permanent (deciding how, maybe a json or a database)
2. When added to a server, automatically choose the server's "main text channel" and add it to the list of listened channels
3. Random message when mentioned
4. When sending an anonymous message theres a way to choose where the message will be sent
5. Add more functions
6. Drastic but reformulate the whole code so it scales well and stays organized, transform events into Cog Classes and take down some amount of code with functions
