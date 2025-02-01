import discord
from discord.ext import commands
from yahoo_fin import stock_info as si

class Trading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prices")
    async def get_futures_price(self, ctx, symbol: str):
        """Fetches real-time price data for a given futures contract and sends it in an embed."""
        futures_mapping = {
            "ES": "^GSPC",   # S&P 500
            "NQ": "^NDX",    # Nasdaq 100
            "GC": "GC=F",    # Gold
            "CL": "CL=F",    # Crude Oil
            "YM": "YM=F",    # Dow Jones
            "SI": "SI=F",    # Silver
        }

        symbol = symbol.upper()
        if symbol not in futures_mapping:
            await ctx.send("Invalid symbol! Available options: ES, NQ, GC, CL, YM, SI")
            return

        ticker = futures_mapping[symbol]
        
        try:
            price = si.get_live_price(ticker)

            # Create an embed message
            embed = discord.Embed(
                title=f"{symbol} Futures Price",
                description=f"**${price:.2f}**",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Data from Yahoo Finance")
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error fetching price: {str(e)}")

async def setup(bot):
    await bot.add_cog(Trading(bot))
