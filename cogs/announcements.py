"""
Author: Ashwin Nair
Date: 2025-01-30
Project name: announcements.py
Summary: For announcements and stock trading signals.
"""

import discord
from discord.ext import commands

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='announce')
    async def announce(self, ctx, *, message: str):
        """Delete the user's message and resend it as an embedded announcement."""
        role_name = "Executive"
        user_roles = [role.name for role in ctx.author.roles]

        if role_name not in user_roles:
            await ctx.send("Access denied. You need the 'executive' role to use this command.")
            return
        else:
            await ctx.message.delete()

            embed = discord.Embed(
                title="📢 Announcement",
                description=message,
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Announced by {ctx.author.display_name}")

            await ctx.send(embed=embed)

    @commands.command(name='call')
    async def call(self, ctx, symbol: str, number: int, position: str, priority: str = None):
        """Send a stock trading signal in the format: !call SYMBOL NUMBER LONG/SHORT [P for priority]"""
        
        role_name = "Executive"
        user_roles = [role.name for role in ctx.author.roles]

        if role_name not in user_roles:
            await ctx.send("Access denied. You need the 'Executive' role to use this command.")
            return

        # Validate position argument
        if position.lower() not in ['long', 'short']:
            await ctx.send("Invalid position. Please use 'long' or 'short'.")
            return

        # Set chart emoji and embed color based on position
        if position.lower() == 'long':
            chart_emoji = "📈"  # Upwards trend for long
            color = discord.Color.green()
        else:
            chart_emoji = "📉"  # Downwards trend for short
            color = discord.Color.red()

        # Set priority and footer
        if priority:
            footer = "Urgent"
            color = discord.Color.gold()  # Yellow color for priority
        else:
            footer = f"Requested by {ctx.author.display_name}"

        # Format the signal message
        signal = f"**{symbol}** {number} **{position.upper()}** {chart_emoji}"

        # Create the embed with the signal
        embed = discord.Embed(
            title="📊 Sora Signal",
            description=signal,
            color=color
        )
        embed.set_footer(text=footer)

        # Send the embed message
        message = await ctx.send(embed=embed)

        # React with thumbs-up and thumbs-down emojis
        await message.add_reaction('👍')
        await message.add_reaction('👎')

        # Delete the user's original call command message
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(Announcements(bot))
