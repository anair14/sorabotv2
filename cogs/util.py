"""
Author: Ashwin Nair
Date: 2025-01-30
Project name: util.py
Summary: Utility functions, including a dynamic help command.
"""

import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Respond with the bot's latency."""
        latency = round(self.bot.latency * 1000)  # Convert to ms
        await ctx.send(f'🏓 Pong! Latency: {latency}ms')

    @commands.command(name='helpme')
    async def help_command(self, ctx):
        """Dynamic help command listing all available commands in an embed."""
        help_embed = discord.Embed(
            title="📚 Bot Commands",
            description="Here are the available commands. Use `!command [arg]` to use them.",
            color=discord.Color.blue()
        )

        # Loop through all cogs and list their commands dynamically
        for cog_name, cog in self.bot.cogs.items():
            commands_list = cog.get_commands()
            if commands_list:
                command_descriptions = '\n'.join(
                    [f"`{ctx.prefix}{cmd.name}`: {cmd.help or 'No description'}" for cmd in commands_list]
                )
                help_embed.add_field(name=f"**{cog_name}**", value=command_descriptions, inline=False)

        # Add a footer for additional info
        help_embed.set_footer(text="Use `!command help` for more details on each command.")

        await ctx.send(embed=help_embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
