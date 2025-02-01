from threading import Thread
from keep_alive import keep_alive
import bot  # Assuming your bot code is in bot.py

def run_bot():
    bot.main()  # Move `bot.run()` inside a `main()` function in bot.py

if __name__ == "__main__":
    # Run the keep-alive server in a separate thread
    Thread(target=keep_alive).start()
    run_bot()
