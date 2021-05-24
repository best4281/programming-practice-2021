import os
import json
import asyncio
import logging
import discord
from discord.ext import commands
from settings import *

#Set up logging: https://discordpy.readthedocs.io/en/stable/logging.html
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

prefixFile = absDir + "/" + prefixFileName

#For getting the member list, you must have intents enabled
intents = discord.Intents.all()

#retrieve prefix of that server
def retrieve_prefix(bot, ctx):
    with open(prefixFile, 'r') as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(ctx.guild.id)]
    except:
        return defaultPrefix

#Set active status of the bot
activity = discord.Activity(type = discord.ActivityType.watching, name = "the world burn 🔥")

#Create an instance of bot
bot = commands.Bot(
    command_prefix = (retrieve_prefix),
    case_insensitive = True,
    intents = intents,
    activity = activity,
)

#Things to do after bot is logged in
@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name} {bot.user.id}")
    for guild in bot.guilds:
        print(f"Belong to guild: {guild.name} {guild.id}")

#Introduce yourself on bot invite and set the prefix for that guild as defaultPrefix
@bot.event
async def on_guild_join(guild):

    with open(prefixFile, 'r') as f:
        prefixes = json.load(f)
        prefixes[str(guild.id)] = defaultPrefix
    with open(prefixFile, 'w') as f:
        json.dump(prefixes, f, indent=4)
    
    await guild.system_channel.send(
        (
        f"Hello people! I am **{bot.user.name}**\n"
        f"You can use my commands with `{defaultPrefix}` as a prefix.\n"
        f"For more info, send `{defaultPrefix}help`"
        )
    )

#Removed saved prefix of the guild that this bot got removed
@bot.event
async def on_guild_remove(guild):
    with open(prefixFile, 'r') as f:
        prefixes = json.load(f)
        prefixes.pop(str(guild.id))
    with open(prefixFile, 'w') as f:
        json.dump(prefixes, f, indent=4)

#Trigger when bot recieve any messages
@bot.event
async def on_message(message):
    if not message.guild:
        await message.author.send("I was not made ready to serve you in private chat, maybe one day I will.")
        return
    await bot.process_commands(message)

#load all the extension in "cogs" folder
if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in os.listdir(absDir + cogsDir) if os.path.isfile(os.path.join(absDir + cogsDir, f)) and not f.startswith('_')]:
        try:
            bot.load_extension("cogs." + extension)
            print(f"{extension} loaded.")
        except (discord.ClientException, ModuleNotFoundError):
            print(f"Failed to load extension {extension}.")

#Run the bot with the given credential
bot.run(discordToken)
