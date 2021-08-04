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

headers = {
    "x-api-key" : API_KEY
}

bot = commands.Bot(command_prefix = "-")

# Connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord')

# Ping command
@bot.command(help = 'Returns connection time')
async def ping(ctx):
    msg = await ctx.channel.send("Pong")
    
    now = datetime.now().timestamp()
    ping = round((now - msg.created_at.timestamp() + 14400) * 1000)
    edit_to = f"Pong, {ping} ms"

    await msg.edit(content = edit_to)

# List command
# Outputs all the supported leagues
@bot.command(help = 'Returns supported leagues')
async def list(ctx):
    response = requests.get("https://esports-api.lolesports.com/persisted/gw/getLeagues?hl=en-US", headers=headers)
    print(response.status_code)

    response_info = response.json()
    leagues = response_info["data"]["leagues"]
    
    result = []
    for league in leagues:
        result.append(league["name"] + "\n")
    await ctx.channel.send("".join(result))

""" # Get schedule command
# Outputs the weekly schedule for the specified league
# arg = league abbreviation (LCS, LEC, etc)
@bot.command(help = 'Returns schedule of specified league')
async def sched(ctx, league):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Please specify which league you would like to see the schedule of (``-list`` for a list of leagues)")
    else:
        await ctx.channel.send("Placeholder, will be pulling from lolesports API") """

bot.run(TOKEN)