import discord
from discord.ext import commands, tasks
from yahoo_fin import stock_info as si

class Trading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.futures_data = {}  # Stores the latest prices
        self.update_prices.start()  # Start the price update loop

    def cog_unload(self):
        """Stops the loop when the cog is unloaded."""
        self.update_prices.cancel()

    @tasks.loop(seconds=5)
    async def update_prices(self):
        """Fetches futures prices every 5 seconds and updates the cache."""
        futures_mapping = {
            "ES": "^GSPC",   # S&P 500
            "NQ": "^NDX",    # Nasdaq 100
            "GC": "GC=F",    # Gold
            "CL": "CL=F",    # Crude Oil
            "YM": "YM=F",    # Dow Jones
            "SI": "SI=F",    # Silver
        }

        for symbol, ticker in futures_mapping.items():
            try:
                self.futures_data[symbol] = si.get_live_price(ticker)
            except Exception as e:
                print(f"Error updating {symbol}: {e}")

    @commands.command(name="prices")
    async def get_futures_price(self, ctx, symbol: str):
        """Sends the latest futures price in an embed."""
        symbol = symbol.upper()
        if symbol not in self.futures_data:
            await ctx.send("Invalid symbol! Available options: ES, NQ, GC, CL, YM, SI")
            return

        price = self.futures_data.get(symbol, "Unavailable")

        embed = discord.Embed(
            title=f"{symbol} Futures Price",
            description=f"💰 **${price:.2f}**",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Updated every 5 seconds | Data from Yahoo Finance")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Trading(bot))
