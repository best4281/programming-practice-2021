#Cogs are like modules of the bot, it was made for easy grouping of commands and listeners (events).

import json
import os
import discord
import aiohttp
from discord.ext import commands
from steam import steamid
from googlesearch import search
from settings import *
#Import from upper directory, because this is a module (I think it is unsafe, but I have no idea)
#It means this file cannot runs on its own, it have to be load from main file to run properly
#I don't know how to import from other directory, still cannot find the answer.

steamDataDir = absDir + "/" + steamDataDir + "/"

#Tag everyone after the search, and create invite
async def send_game_invite(ctx, game:str, appid:str, users:list):
    mentions = ' '.join("<@" + str(user) + ">" for user in users)
    embed = discord.Embed(title = "Let's come together and play **" + game + "**.", description = "steam://run/" + appid, color = 0X6ef9f5)
    await ctx.send(mentions, embed = embed)

#Search steam game by appid
async def search_by_appid(ctx, members, appid, **kwargs):
    appidstr = str(appid)
    ownedMembers = []
    async with aiohttp.ClientSession() as session:
        #Request the app detail from steam website
        async with session.get("https://store.steampowered.com/api/appdetails?appids=" + appidstr) as response:
            #search for app name
            if response.status != 200:
                #If it was not searched by search_by_keyword() before
                if "app" not in kwargs:
                    await ctx.send("**" + appidstr + "** cannot be verified with Steam, is Steam API down?")
                    return
            game = await response.json()
        #If steam website respond with nothing
        if game == None:
            #If it was not searched by search_by_keyword() before
            if "app" not in kwargs:
                await ctx.send("**" + appidstr + "** is not a valid appid for any availble Steam applications.")
                return
        #If steam said it was not success
        if not game[appidstr]["success"]:
            if "app" not in kwargs:
                await ctx.send("**" + appidstr + "** is not a valid appid for any availble Steam applications.")
                return
    try:
        #If there is game name from the search, use it.
        gameName = game[appidstr]["data"]["name"]
    except:
        #If there is still no game name, use the rough name from the link (without underscore)
        gameName = kwargs["app"]
    #Check everyone data and search for target appid
    for member in members:
        try:
            userData = json.load(open(steamDataDir + str(member) + ".json", 'r'))["games"]
            for app in userData:
                if app["appid"] == appid:
                    ownedMembers.append(member)
                    break
        except:
            pass
    #If no one is in the list
    if not ownedMembers:
        await ctx.send("Sadly, nobody registered with me here has **" + gameName + "** in their steam library.")
        return
    #If there is people in the list
    await send_game_invite(ctx, gameName, appidstr, ownedMembers)

#Search game by given keyword
async def search_by_keyword(ctx, members, keyword):
    try:
        #Use google search (This gives 429 too easy, so the "pause" should be there)
        matched = search(keyword + " site:store.steampowered.com/app/", tld="com", lang = "en", num=1, start = 0, stop  = 1, pause = 2)
        found = False
        for link in matched:
            found = True
            appID = link.split('/')[4]
            roughAppName = link.split('/')[5].replace('_', ' ')
            try:
                appidnum = int(appID)
            except:
                #If somehow the gotten link is not in normal format. Example: (https://store.steampowered.com/app/289070/Sid_Meiers_Civilization_VI/)
                appidnum = [int(part) for part in link.split('/') if part.isdigit()]
                if not appidnum:
                    appidnum = appidnum[0]
                    print("seriously?")
                else:
                    #If out of luck from google searh, I don't know...
                    await ctx.send(":robot: **Beep Boop** Google has tricked me and now I am broken inside.")
    except Exception as e:
        #For catching unexpected error
        await ctx.send(e)
        return
    #If no result were found
    if not found:
        await ctx.send("**" + keyword + "** does not match any apps on Steam, please try again with different keyword or use appid instead.")
        return
    #Use gotten appid to continue searching.
    await search_by_appid(ctx, members, appidnum, app = roughAppName)


class steamInteractionCog(commands.Cog, name = "Steam", description = "Commands for interacting with Steam"):
    

    def __init__(self,bot):
        self.bot = bot
        self.description = (
            "`steam_profile_link:` link to your steam profile (Steam library visibility must be set to public)\n"
            "`disconnect` or `dc:` unlink your linked steam profile\n"
            "(You have to connect it manually, since using bot to retrieve the connected Steam account is against Discord privacy policy)\n"
            "*By executing this commands and successfully connect your Steam account to this bot, you have fully agree to privacy policy of this bot (which we have none)*"
        )
    
    #Connect steam profile to this bot
    @commands.command(
        name = "steamconnect",
        aliases = ["sc"],
        help = "Connect Steam Library data to Discord account",
        usage = "<steam_profile_link/disconnect/dc>",
    )
    async def steam_connect(self, ctx, steamURL = None):

        #Send help message when no link is provided
        if steamURL == None:
            await ctx.send(self.description)
            return
        
        #Remove saved data when "dc" or "disconnect" is passed after command like `!steamconnect disconnect`
        if steamURL.lower() == "dc" or steamURL.lower() == "disconnect":
            userFile = steamDataDir + str(ctx.author.id) + ".json"
            #If the file for that user already exists
            if os.path.isfile(userFile):
                os.remove(userFile)
                await ctx.send(ctx.author.mention + f"Your Steam Library data has been removed from this bot. To reconnect, use `{get_prefix(ctx)}steamconnect <steam_profile_link>`.")
                return
            #If the file for that user does not exist
            else:
                await ctx.send(ctx.author.mention + f"Your Steam Library data does not belong to us (yet). You can connect using `{get_prefix(ctx)}steamconnect <steam_profile_link>`.")
                print(f"Error: {userFile} file not found")
                return
        
        #For showing that the bot is doing some calculation
        async with ctx.typing():
            try:
                #Retrieve absolute steam ID
                steamID = steamid.from_url(steamURL).as_64
            except Exception as e:
                print(e)
                await ctx.send(ctx.author.mention + "Your steam ID is irretrievable; the link may be invalid or Steam Web API might be down.")
                return
            if steamID == None:
                await ctx.send(ctx.author.mention + "Your steam ID is irretrievable; the link may be invalid or Steam Web API might be down.")
                return
            async with aiohttp.ClientSession() as session:
                #Get steam library of the provided link
                async with session.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + str(steamToken) + "&steamid=" + str(steamID) + "&include_played_free_games=1&format=json") as response:
                    if response.status != 200:
                        await ctx.send("Cannot retrieve game list from steam for " + ctx.author.mention + ". Is steam Web API down?")
                        return
                    ownedGames = await response.json()
                #If response is not exist
                if "response" not in ownedGames.keys():
                    await ctx.send("Cannot retrieve game list from steam for " + ctx.author.mention + ". Is steam Web API down?")
                    return
                #If there is no game count, it means the data for steam library is private.
                if "game_count" not in ownedGames["response"].keys() or ownedGames["response"]["game_count"] <= 0:
                    await ctx.send(ctx.author.mention + " Steam library data is private, please change your privacy setting in Steam")
                    return
                #Format data for saving in json file
                ownedGames["discord_id"] = ctx.author.id
                ownedGames["steam_id"] = steamID
                ownedGames["game_count"] = ownedGames["response"].pop("game_count")
                ownedGames["games"] = []
                for game in ownedGames["response"]["games"]:
                    newInfo = {}
                    newInfo["appid"] = game["appid"]
                    newInfo["playtime_forever"] = game["playtime_forever"]
                    game.clear()
                    ownedGames["games"].append(newInfo)
                    del newInfo
                del(ownedGames["response"])
                #Save the data to json file
                json.dump(ownedGames, open(steamDataDir + str(ctx.author.id) + ".json", 'w'), indent = 4)
                async with session.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + str(steamToken) + "&steamids=" + str(steamID) + "&format=json") as response:
                    #get the player name, just for friendliness of acknowledging user
                    if response.status != 200:
                        await ctx.send(ctx.author.mention + " Your Steam library was tied to Discord account successfully.")
                        return
                    steamUser = await response.json()
        try:
            await ctx.send(ctx.author.mention + " Steam library from **" + steamUser["response"]["players"][0]["personaname"] + "** was tied to your Discord account successfully.")
        except:
            await ctx.send(ctx.author.mention + " Steam library was tied to Discord account successfully.")

    #Command to search for a game
    @commands.command(
        name = "tagbygame",
        aliases = ["tg","tag"],
        help = "Mention people with the game in their Steam library.",
        usage = "<search_keyword/appid>",
        description = (
            "`search_keyword:` keyword to search for game\n"
            "`appid:` application ID of application on steam\n\n"
            "This will only mention everyone who has connected Steam Library to this bot that has the game you searched for.\n⠀"
        )
    )
    @commands.guild_only()
    async def tag_steam(self, ctx, *args):
        prefix = get_prefix(ctx)
        
        #Send help if no search keyword is provided
        if not args:
            await ctx.send(self.description)
            return
        
        #Get all the members in the server that the message was sent from
        membersID = [member.id for member in ctx.guild.members if not member.bot]
        keyword = ' '.join(args)
        
        try:
            #There is no game that are full of number, so it must be searching using appid if the input is all number
            appID = int(keyword)
            async with ctx.typing():
                await search_by_appid(ctx, membersID, appID)
        except:
            async with ctx.typing():
                await search_by_keyword(ctx, membersID, keyword)

#Entry point for the main file to load up this extension
def setup(bot):
    bot.add_cog(steamInteractionCog(bot))
