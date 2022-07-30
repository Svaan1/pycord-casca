import discord
import io
import aiohttp

# Config Variables
main_channel_id = 0
channels_to_listen = []
people_to_annoy = []

# Client Creation
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents = intents)

# Events
@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="you")
    await client.change_presence(activity=activity)
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if isinstance(message.channel, discord.DMChannel):
        channel = client.get_channel(main_channel_id)

        if message.attachments:
            my_url = message.attachments[0].url
            async with aiohttp.ClientSession() as session:
                async with session.get(my_url) as resp:
                    if resp.status != 200:
                        return await channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await channel.send(file=discord.File(data, 'cool_image.png'))
        else:
            await channel.send("Anonymous Message: " + message.content)
    
    if message.channel.id in channels_to_listen:
        if client.user.mentioned_in(message):
            await message.channel.send('Desired mention message', reference=message)
        elif message.author.id in people_to_annoy:
            channel = client.get_channel(message.channel.id)
            await message.add_reaction("🤣")

# Start Bot
client.run('your discord token here')