import discord
from discord.ext import commands, tasks
from yahoo_fin import stock_info as si

class Trading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.futures_data = {}  # Stores the latest prices
        self.alerts = {}  # Stores active price alerts
        self.alert_users = {}  # Stores users who set the alerts
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

        price = self.futures_data.get(symbol, "Unavailable")

        if price == "Unavailable":
            await ctx.send(f"Real-time data for {symbol} is currently unavailable.")
            return

        embed = discord.Embed(
            title=f"{symbol} Futures Price",
            description=f"**${price:.2f}**",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Updated every 5 seconds | Data from Yahoo Finance")

        await ctx.send(embed=embed)

    @commands.command(name="trend")
    async def get_moving_average(self, ctx, symbol: str, period: int):
        """Fetches the Simple Moving Average (SMA) of a futures contract."""
        symbol = symbol.upper()

        try:
            # Get historical data and calculate SMA
            data = si.get_data(symbol)
            sma = data['close'].rolling(window=period).mean().iloc[-1]
            await ctx.send(f"The {period}-period SMA for {symbol} is ${sma:.2f}")
        except Exception as e:
            await ctx.send(f"Error fetching data: {str(e)}")

    @commands.command(name="set_alert")
    async def set_price_alert(self, ctx, symbol: str, target_price: float):
        """Set a price alert for a specific futures contract."""
        symbol = symbol.upper()

        if symbol not in self.futures_data:
            await ctx.send("Invalid symbol! Use the `prices` command to see available symbols.")
            return

        if symbol not in self.alerts:
            self.alerts[symbol] = []
            self.alert_users[symbol] = []

        self.alerts[symbol].append(target_price)
        self.alert_users[symbol].append(ctx.author)
        await ctx.send(f"Price alert set for {symbol} at ${target_price:.2f}")

    @tasks.loop(seconds=5)
    async def check_alerts(self):
        """Check if any price alerts should be triggered."""
        for symbol, prices in self.alerts.items():
            current_price = self.futures_data.get(symbol, None)
            if current_price is None:
                continue

            for target_price, user in zip(prices, self.alert_users[symbol]):
                if (current_price >= target_price):
                    await user.send(f"Alert: {symbol} has reached or exceeded your target price of ${target_price:.2f}!")
                    self.alerts[symbol].remove(target_price)
                    self.alert_users[symbol].remove(user)

async def setup(bot):
    await bot.add_cog(Trading(bot))

