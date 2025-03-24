import telebot
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://localhost:8001/chat/"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Hallo! Ik ben jouw Nederlandse leerassistent. Typ een zin en ik zal helpen!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    response = requests.post(API_URL, json={"message": user_text}).json()
    bot.reply_to(message, response["response"])

@bot.message_handler(content_types=["voice"])
def voice(message):
    bot.reply_to(message, "Ik kan geen spraakberichten verwerken. Stuur me een tekstbericht.")

if __name__ == "__main__":
    bot.polling()

# The bot.py script uses the Telebot library to create a Telegram bot that interacts with the Dutch Learning AI Bot.`
# The bot.py script imports the Telebot library and the requests library.
# The bot.py script defines the TELEGRAM_TOKEN and API_URL variables.
# The bot.py script creates a Telebot object named bot.
# The bot.py script defines a message handler that replies to the /start command with a welcome message.
# The bot.py script defines a message handler that sends user input to the Dutch Learning AI Bot API and replies with the response.
# The bot.py script starts the bot by calling the bot.polling() method.
# The bot.py script runs the bot when executed.
# The bot.py script interacts with the Dutch Learning AI Bot API to chat with users on Telegram.
# The bot.py script uses the requests library to send POST requests to the Dutch Learning AI Bot API.
# The bot.py script uses the Telebot library to create a Telegram bot that interacts with users.