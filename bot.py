import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I am alive 🚀")

def main():
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise ValueError("No DISCORD_BOT_TOKEN environment variable set")
    bot.run(TOKEN)
