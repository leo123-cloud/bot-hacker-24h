import telebot
from telebot import types
import datetime
import logging
import random
import time

# --- CONFIGURAZIONE LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CORE CONFIG ---
API_TOKEN = '8461004019:AAHKN207J0ot8LKlc7t8CVhHiQ2xz4t0ua8'
PASSWORD_SEGRETA = "123leo123"
bot = telebot.TeleBot(API_TOKEN)

user_authenticated = {}

# --- DATABASE STRUMENTI (TITAN 1000) ---
DATABASE = {
    "phishing": {
        "zphisher": {"name": "🛡️ ZPHISHER", "cmd": "git clone https://github.com/htr-tech/zphisher\ncd zphisher\nbash zphisher.sh"},
        "advphishing": {"name": "🎣 ADVPHISHING", "cmd": "git clone https://github.com/AbirHasan2005/AdvPhishing\ncd AdvPhishing\nbash setup.sh\n./AdvPhishing.sh"}
    },
    "osint": {
        "seeker": {"name": "📍 SEEKER GPS", "cmd": "git clone https://github.com/thewhiteh4t/seeker\ncd seeker\npython3 seeker.py"},
        "sherlock": {"name": "🕵️ SHERLOCK", "cmd": "git clone https://github.com/sherlock-project/sherlock\ncd sherlock\npython3 sherlock.py [user]"}
    },
    "web": {
        "sqlmap": {"name": "💉 SQLMAP", "cmd": "git clone https://github.com/sqlmapproject/sqlmap\ncd sqlmap\npython3 sqlmap.py"},
        "nmap": {"name": "🔍 NMAP", "cmd": "pkg install nmap -y\nnmap -v -A [target]"}
    }
}

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🎣 PHISHING", callback_data="cat_phishing"),
               types.InlineKeyboardButton("🕵️ OSINT", callback_data="cat_osint"),
               types.InlineKeyboardButton("🌐 WEB ATTACK", callback_data="cat_web"),
               types.InlineKeyboardButton("📡 STATUS", callback_data="status"),
               types.InlineKeyboardButton("🔒 LOCK", callback_data="lock"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if uid in user_authenticated and user_authenticated[uid]:
        bot.send_message(message.chat.id, "✅ Console Attiva.", reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "🔐 **SISTEMA TITAN**\nInserisci la password:")
        bot.register_next_step_handler(message, check_auth)

def check_auth(message):
    if message.text == PASSWORD_SEGRETA:
        user_authenticated[message.from_user.id] = True
        bot.send_message(message.chat.id, "🔓 **ACCESSO GARANTITO**", reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "❌ Errata. Usa /start")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    uid = call.from_user.id
    if uid not in user_authenticated or not user_authenticated[uid]: return

    if call.data == "home":
        bot.edit_message_text("🛸 **SELECT MODULE**", call.message.chat.id, call.message.message_id, reply_markup=main_menu())
    elif "cat_" in call.data:
        cat = call.data.replace("cat_", "")
        markup = types.InlineKeyboardMarkup()
        for k in DATABASE[cat]:
            markup.add(types.InlineKeyboardButton(DATABASE[cat][k]["name"], callback_data=f"tool_{cat}_{k}"))
        markup.add(types.InlineKeyboardButton("⬅️ MENU", callback_data="home"))
        bot.edit_message_text(f"📂 **SISTEMA {cat.upper()}**", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif "tool_" in call.data:
        _, cat, k = call.data.split("_")
        tool = DATABASE[cat][k]
        bot.edit_message_text(f"💻 **{tool['name']}**\n\n`{tool['cmd']}`", call.message.chat.id, call.message.message_id, 
                             reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("⬅️ BACK", callback_data=f"cat_{cat}")))

bot.polling(none_stop=True)
