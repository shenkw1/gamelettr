import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = "-")

client = discord.Client()

# Ping command
@bot.command()
async def ping(ctx):
    msg = await ctx.channel.send("Pong")
    
    now = datetime.now().timestamp()
    ping = round((now - msg.created_at.timestamp() + 14400) * 1000)
    edit_to = f"Pong, {ping} ms"

    await msg.edit(content = edit_to)

bot.run(TOKEN)