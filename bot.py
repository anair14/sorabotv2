import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

# Async function to load cogs
async def load_cogs():
    # List of cog names to load
    cogs = ["cogs.announcements", "cogs.util"]
    
    for cog in cogs:
        try:
            await bot.load_extension(cog)  # Make sure to await loading cogs
            print(f"Loaded cog: {cog}")
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I am alive 🚀")

def main():
    bot.loop.create_task(load_cogs())
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise ValueError("No DISCORD_BOT_TOKEN environment variable set")
    bot.run(TOKEN)
