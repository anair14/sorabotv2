import discord
from discord.ext import commands, tasks
from yahoo_fin import stock_info as si
import requests
 
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
        if symbol not in self.futures_data:
            await ctx.send("Invalid symbol! Available options: ES, NQ, GC, CL, YM, SI")
            return
 
        try:
            # Get historical data and calculate SMA
            data = si.get_data(symbol)
            sma = data['close'].rolling(window=period).mean()[-1]
            await ctx.send(f"The {period}-period SMA for {symbol} is ${sma:.2f}")
        except Exception as e:
            await ctx.send(f"Error fetching data: {str(e)}")
 
    @commands.command(name="historical")
    async def get_historical_data(self, ctx, symbol: str, timeframe: str):
        """Fetches historical data for a given futures contract."""
        symbol = symbol.upper()
        if symbol not in self.futures_data:
            await ctx.send("Invalid symbol! Available options: ES, NQ, GC, CL, YM, SI")
            return
 
        try:
            data = si.get_data(symbol, period=timeframe)  # Options: '1d', '5d', '1mo', etc.
            data_str = data[['close']].tail(5).to_string()  # Show last 5 data points
            await ctx.send(f"Historical data for {symbol}:\n{data_str}")
        except Exception as e:
            await ctx.send(f"Error fetching data: {str(e)}")
 
    @commands.command(name="alerts")
    async def set_alert(self, ctx, symbol: str, price: float):
        """Set a price alert for a futures contract."""
        symbol = symbol.upper()
        if symbol not in self.futures_data:
            await ctx.send("Invalid symbol! Available options: ES, NQ, GC, CL, YM, SI")
            return
 
        # Store the alert and associate the user with it
        self.alerts[symbol] = price
        self.alert_users[symbol] = ctx.author
        await ctx.send(f"Price alert for {symbol} set at ${price:.2f}. You will be notified in DMs.")
 
    @tasks.loop(seconds=5)
    async def check_alerts(self):
        """Checks if any price alerts have been triggered and sends a DM to the user."""
        for symbol, target_price in self.alerts.items():
            current_price = self.futures_data.get(symbol)
            if current_price and current_price >= target_price:
                # Send DM to the user who set the alert
                user = self.alert_users.get(symbol)
                if user:
                    try:
                        await user.send(f"🚨 **Price Alert**: {symbol} has reached ${current_price:.2f}, which is above your set alert of ${target_price:.2f}.")
                    except discord.errors.Forbidden:
                        await user.send("I couldn't send the alert because your DMs are closed.")
                # Remove the alert after it triggers
                del self.alerts[symbol]
                del self.alert_users[symbol]
 
    @commands.command(name="news")
    async def get_futures_news(self, ctx, symbol: str):
        """Fetches the latest news related to a futures contract."""
        symbol = symbol.upper()
        if symbol not in self.futures_data:
            await ctx.send("Invalid symbol! Available options: ES, NQ, GC, CL, YM, SI")
            return
 
        # Use an external news API (e.g., NewsAPI)
        api_key = 'YOUR_NEWSAPI_KEY'
        url = f'https://newsapi.org/v2/everything?q={symbol}&apiKey={api_key}'
 
        try:
            response = requests.get(url).json()
            articles = response['articles'][:3]  # Get the top 3 articles
            if not articles:
                await ctx.send(f"No recent news for {symbol}.")
            else:
                news = "\n".join([f"**{article['title']}**\n{article['url']}" for article in articles])
                await ctx.send(f"Latest news for {symbol}:\n{news}")
        except Exception as e:
            await ctx.send(f"Error fetching news: {str(e)}")
 
    @commands.command(name="volume")
    async def get_volume(self, ctx, symbol: str):
        """Displays the current trading volume for a futures contract."""
        symbol = symbol.upper()
        if symbol not in self.futures_data:
            await ctx.send("Invalid symbol! Available options: ES, NQ, GC, CL, YM, SI")
            return
 
        try:
            data = si.get_data(symbol)
            volume = data['volume'].iloc[-1]  # Latest volume
            await ctx.send(f"The latest trading volume for {symbol} is {volume:,} contracts.")
        except Exception as e:
            await ctx.send(f"Error fetching volume: {str(e)}")
 
async def setup(bot):
    await bot.add_cog(Trading(bot))
