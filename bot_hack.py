import telebot
from telebot import types

API_TOKEN = '8461004019:AAHKN207J0ot8LKlc7t8CVhHiQ2xz4t0ua8'
bot = telebot.TeleBot(API_TOKEN)

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🌐 Zphisher", callback_data='z1'),
        types.InlineKeyboardButton("📍 Seeker", callback_data='s1'),
        types.InlineKeyboardButton("🔍 Infoga", callback_data='i1'),
        types.InlineKeyboardButton("💣 DarkFly", callback_data='d1')
    )
    return markup

def back_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ TORNA AL MENU", callback_data='home'))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    testo = "🥷 **SISTEMA ATTIVO** 🔓\n\nScegli un modulo da iniettare:"
    bot.reply_to(message, testo, reply_markup=main_menu(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'home':
        bot.edit_message_text("⚙️ **MENU PRINCIPALE**", call.message.chat.id, call.message.message_id, reply_markup=main_menu(), parse_mode='Markdown')
    elif call.data == 'z1':
        res = "🚀 **ZPHISHER**\n\n📥 **INSTALLA**:\n`pkg install git php -y`\n`git clone https://github.com/htr-tech/zphisher`\n\n▶️ **LANCIO**:\n`cd zphisher` && `bash zphisher.sh`"
        bot.edit_message_text(res, call.message.chat.id, call.message.message_id, reply_markup=back_button(), parse_mode='Markdown')
    elif call.data == 's1':
        res = "📡 **SEEKER**\n\n📥 **INSTALLA**:\n`pkg install git python php -y`\n`git clone https://github.com/thewhiteh4t/seeker`\n\n▶️ **LANCIO**:\n`cd seeker` && `python3 seeker.py`"
        bot.edit_message_text(res, call.message.chat.id, call.message.message_id, reply_markup=back_button(), parse_mode='Markdown')
    elif call.data == 'i1':
        res = "🔍 **INFOGA**\n\n📥 **INSTALLA**:\n`pkg install git python -y`\n`git clone https://github.com/m4ll0k/Infoga`\n\n▶️ **LANCIO**:\n`cd Infoga` && `python3 infoga.py`"
        bot.edit_message_text(res, call.message.chat.id, call.message.message_id, reply_markup=back_button(), parse_mode='Markdown')
    elif call.data == 'd1':
        res = "💣 **DARKFLY**\n\n📥 **INSTALLA**:\n`pkg install git python2 -y`\n`git clone https://github.com/Ranginang67/DarkFly-Tool`\n\n▶️ **LANCIO**:\n`cd DarkFly-Tool` && `python2 install.py`"
        bot.edit_message_text(res, call.message.chat.id, call.message.message_id, reply_markup=back_button(), parse_mode='Markdown')

bot.polling()
