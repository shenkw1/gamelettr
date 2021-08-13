import os
import discord
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY')

HEADERS = {
    "x-api-key" : API_KEY
}

bot = commands.Bot(command_prefix = "-")

ROOT_URL = "https://esports-api.lolesports.com/persisted/gw/"

# Connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')

# Ping command
@bot.command(help='Returns connection time')
async def ping(ctx):
    msg = await ctx.channel.send("Pong")
    
    now = datetime.now().timestamp()
    ping = round((now - msg.created_at.timestamp() + 14400) * 1000) # math to fix difference from UTC
    edit_to = f"Pong, {ping} ms"

    await msg.edit(content=edit_to)

# List command
# Outputs all the supported leagues, organized by region in embed menu
@bot.command(help="Returns supported leagues")
async def list(ctx):
    response = requests.get(ROOT_URL + "getLeagues?hl=en-US", headers=HEADERS)

    if response.status_code != 200:
        await ctx.channel.send("Something went wrong, please try again later...")
        return

    response_info = response.json()
    leagues = response_info["data"]["leagues"]
    
    # Organizing data and adding it to hashmap
    regions = {}
    for league in leagues:
        region = league["region"]
        league_name = league["name"]

        if region not in regions:
            regions[region] = []
        
        regions[region].append(league_name)
    
    # Creating embed
    embed = discord.Embed(title="Supported leagues", color=discord.Color.blurple())
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1407732613171793925/pQZWynfn_400x400.jpg")

    for region in regions:
        formatted_str = ", ".join(regions[region])
        if region == "COMMONWEALTH OF INDEPENDENT STATES":
            embed.add_field(name="CONTINENTAL", value=formatted_str, inline=True)
        else:
            embed.add_field(name=region, value=formatted_str, inline=(region!="EUROPE"))
    
    # Adding empty character to fix column alignment in embed
    v = 3 - ((len(regions) - 1) % 3)
    for _ in range(v):
        embed.add_field(name = "\u200b", value= "\u200b")

    await ctx.channel.send(embed=embed)

bot.run(TOKEN)