import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{client.user} has connected to Discord')

client = CustomClient()
client.run(TOKEN)