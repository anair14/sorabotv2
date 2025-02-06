"""
Author: Ashwin Nair
Date: 2025-01-30
Project name: bot.py
Summary: Main file for the bot.
"""

import discord
from discord.ext import commands
import json
import os


TOKEN = os.getenv('TOKEN')

# Load configuration
with open("config.json") as config_file:
    config = json.load(config_file)

# Enable all intents
intents = discord.Intents.default()
intents.messages = True  # Ensure message-related events are enabled
intents.message_content = True  # Required for reading message content in commands

# Bot setup
bot = commands.Bot(command_prefix=config["prefix"], intents=intents, help_command=None)

# Load cogs asynchronously
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
