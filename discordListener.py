import discord
import os
from dotenv import load_dotenv
import classes.DiscordHelper as dh

discordHelper = dh.DiscordHelper()
load_dotenv('.env')
intents=discord.Intents.default()
client=discord.Client(intents=intents)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return
    substr = str(message.content)
    cmdIDX = substr.find(" ")
    if cmdIDX == -1:
        return
    else:
        command = substr[0:cmdIDX]
        argument = substr[cmdIDX+1:]
    
    if discordHelper.isValidCommand(command) and discordHelper.isAuthorized(message.author):
        await discordHelper.executeCommand(command, argument, message.author, channel)

client.run(os.getenv('DISCORD_TOKEN'))