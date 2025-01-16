from bot.handlers import bot
from bot.database import initialize_database

def main():
    initialize_database()
    print("Bot is running...")
    bot.infinity_polling()

if __name__ == "__main__":
    main()
