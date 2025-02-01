import asyncio
from threading import Thread
from keep_alive import keep_alive
import bot  # Assuming your bot code is in bot.py

async def run_bot():
    await bot.main()  # Ensure bot.main() is awaited

if __name__ == "__main__":
    # Run the keep-alive server in a separate thread
    Thread(target=keep_alive).start()

    # Run the bot asynchronously
    asyncio.run(run_bot())  # Use asyncio.run() to run the bot asynchronously
