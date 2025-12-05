import os
import telebot
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# 🔹 Replace with your actual bot token from BotFather
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 🔹 Replace with your Discord Webhook URL
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    """Sends a welcome message with a 'Share Contact' button."""
    markup = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True
    )
    button = telebot.types.KeyboardButton("📱 Share Your Contact", request_contact=True)
    markup.add(button)

    bot.send_message(
        message.chat.id,
        "Hello! Please share your phone number by clicking the button below. 📲",
        reply_markup=markup,
    )


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    """Handles the shared contact and sends a confirmation message."""
    if message.contact:
        # Extract user details
        user_id = message.contact.user_id
        first_name = message.contact.first_name or "Unknown"
        last_name = message.contact.last_name or ""
        username = message.chat.username or "No Username"
        phone_number = message.contact.phone_number
        chat_type = "Private" if message.chat.type == "private" else "Group"
        message_time = datetime.utcfromtimestamp(message.date).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )

        # Send data to Discord
        data = {
            "content": f"""
📞 **New Contact Received!**
👤 **Name:** {first_name} {last_name}
🆔 **User ID:** {user_id}
📱 **Phone Number:** {phone_number}
🔗 **Username:** @{username}
💬 **Chat Type:** {chat_type}
⏰ **Received At:** {message_time}
            """
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)

        # Confirm in Telegram
        bot.send_message(
            message.chat.id,
            f"✅ Thank you, {first_name}! Your phone number has been received.",
        )


bot.polling()
