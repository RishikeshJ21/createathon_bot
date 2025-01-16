import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def fetch_challenge_data():
    API_URL = os.getenv("API_URL")
    try:
        response = requests.get(f"{API_URL}/challenge/")
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching challenge data: {e}")
        return []

def send_challenge_slider(chat_id, bot, current_index, user_states):
    challenges = fetch_challenge_data()
    if current_index >= len(challenges):
        bot.send_message(chat_id, "End of Challenges.")
        return
    challenge = challenges[current_index]
    markup = InlineKeyboardMarkup()
    if current_index > 0:
        markup.add(InlineKeyboardButton("Previous", callback_data=f"challenge_{current_index - 1}"))
    if current_index < len(challenges) - 1:
        markup.add(InlineKeyboardButton("Next", callback_data=f"challenge_{current_index + 1}"))
    bot.send_message(
        chat_id,
        f"Challenge {current_index + 1}: {challenge}",
        reply_markup=markup
    )
    user_states[chat_id]["challenge_index"] = current_index