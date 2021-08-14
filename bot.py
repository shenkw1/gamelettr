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

# Getting leagues from API data
response = requests.get(ROOT_URL + "getLeagues?hl=en-US", headers=HEADERS)
response_info = response.json()
leagues = response_info["data"]["leagues"]
    
# Organizing data and adding it to region-league hashmap, and adding IDs to list
regions = {}
ids = []
imgs = []
for league in leagues:
    region = league["region"]
    league_name = league["name"]
    league_id = league["id"]
    league_image = league["image"]

    if region not in regions:
        regions[region] = []
            
    regions[region].append(league_name)
    ids.append(league_id)
    imgs.append(league_image)

# Connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')

# Ping command
@bot.command(help='Returns connection time')
async def ping(ctx):
    msg = await ctx.channel.send("Pong")
    
    now = datetime.now().timestamp()
    ping = round(bot.latency * 1000)
    edit_to = f"Pong, {ping} ms"

    await msg.edit(content=edit_to)

# List command
# Outputs all the supported leagues, organized by region in embed menu
@bot.command(help="Returns supported leagues")
async def list(ctx):    
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