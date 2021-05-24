import os
import json
from dotenv import load_dotenv

prefixFileName = "prefixes.json"
cogsDir = "/cogs"
defaultPrefix = '!'
botColor = 0xafff00

load_dotenv()
discordToken = os.getenv("DISCORD_TOKEN")
steamToken = os.getenv("STEAM_WEB_API_KEY")
steamDataDir = os.getenv("STEAM_DATA_DIR")

absDir = os.path.abspath(os.path.dirname(__file__))

try:
    os.mkdir(absDir + "/" + steamDataDir)
except OSError:
    pass

def get_prefix(ctx):
    with open(absDir + '/' + prefixFileName, 'r') as f:
        prefixes = json.load(f)
    try:
        return prefixes[str(ctx.guild.id)]
    except:
        return defaultPrefix

if __name__ == "__main__":
    print(absDir)