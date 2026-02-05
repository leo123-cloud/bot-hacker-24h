import telebot
from telebot import types

API_TOKEN = '8461004019:AAHKN207J0ot8LKlc7t8CVhHiQ2xz4t0ua8'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🛡️ Zphisher", callback_data='zphisher_cmd')
    btn2 = types.InlineKeyboardButton("📍 Seeker", callback_data='seeker_cmd')
    btn3 = types.InlineKeyboardButton("🎣 Nexphisher", callback_data='nexphisher_cmd')
    btn4 = types.InlineKeyboardButton("🐍 PyPhisher", callback_data='pyphisher_cmd')
    markup.add(btn1, btn2, btn3, btn4)
    bot.reply_to(message, "🔥 **BENVENUTO NEL BOT HACKER** 🔥\nScegli un tool per info e comandi:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    markup = types.InlineKeyboardMarkup()
    if "_cmd" in call.data:
        tool = call.data.replace("_cmd", "")
        desc = {
            "zphisher": "🛡️ **ZPHISHER**: Crea pagine web identiche ai social per testare la sicurezza delle password. Include 30+ template.",
            "seeker": "📍 **SEEKER**: Invia un link che, se cliccato, ti mostra la posizione GPS esatta della vittima.",
            "nexphisher": "🎣 **NEXPHISHER**: Versione evoluta di Zphisher, più veloce e stabile per Termux.",
            "pyphisher": "🐍 **PYPHISHER**: Tool Python con 77 template e sistema per nascondere i link."
        }
        cmds = {
            "zphisher": "`git clone https://github.com/htr-tech/zphisher` \n`cd zphisher` \n`bash zphisher.sh`",
            "seeker": "`git clone https://github.com/thewhiteh4t/seeker` \n`cd seeker` \n`python3 seeker.py`",
            "nexphisher": "`git clone https://github.com/htr-tech/nexphisher` \n`cd nexphisher` \n`bash nexphisher.sh`",
            "pyphisher": "`git clone https://github.com/KasRoudra/PyPhisher` \n`cd PyPhisher` \n`python3 pyphisher.py`"
        }
        text = f"{desc[tool]}\n\n💻 **COMANDI**:\n{cmds[tool]}"
        back_btn = types.InlineKeyboardButton("⬅️ TORNA AL MENU", callback_data='home')
        markup.add(back_btn)
    elif call.data == "home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message)
        return
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

bot.polling()
