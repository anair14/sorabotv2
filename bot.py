import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

# Async function to load cogs
async def load_cogs():
    # List of cog names to load
    cogs = ["cogs.announcements", "cogs.util"]
    
    for cog in cogs:
        try:
            await bot.load_extension(cog)  # Await loading cogs asynchronously
            print(f"Loaded cog: {cog}")
        except Exception as e:
            print(f"Failed to load cog {cog}: {e}")

# Main async function to run the bot
async def main():
    # Load cogs asynchronously
    await load_cogs()

    # Run the bot
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("No DISCORD_BOT_TOKEN environment variable set")
    
    await bot.start(TOKEN)  # Use `await bot.start()` instead of `bot.run()`

if __name__ == "__main__":
    # Run the main async function with asyncio.run()
    asyncio.run(main())
