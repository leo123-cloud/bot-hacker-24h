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
    bot.reply_to(message, "🔥 **BENVENUTO** 🔥\nScegli un tool:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        markup = types.InlineKeyboardMarkup()
        if "_cmd" in call.data:
            tool = call.data.replace("_cmd", "")
            cmds = {
                "zphisher": "`git clone https://github.com/htr-tech/zphisher` \n`cd zphisher` \n`bash zphisher.sh`",
                "seeker": "`git clone https://github.com/thewhiteh4t/seeker` \n`cd seeker` \n`python3 seeker.py`",
                "nexphisher": "`git clone https://github.com/htr-tech/nexphisher` \n`cd nexphisher` \n`bash nexphisher.sh`",
                "pyphisher": "`git clone https://github.com/KasRoudra/PyPhisher` \n`cd PyPhisher` \n`python3 pyphisher.py`"
            }
            text = f"💻 **COMANDI {tool.upper()}**:\n{cmds[tool]}"
            info_btn = types.InlineKeyboardButton("ℹ️ INFORMAZIONI", callback_data=f"{tool}_info")
            back_btn = types.InlineKeyboardButton("⬅️ MENU", callback_data='home')
            markup.add(info_btn, back_btn)
        elif "_info" in call.data:
            tool = call.data.replace("_info", "")
            desc = {
                "zphisher": "ℹ️ **INFO ZPHISHER**: Crea pagine clone di social come FB o IG per testare password. Ha oltre 30 template pronti.",
                "seeker": "ℹ️ **INFO SEEKER**: Invia un link esca per ottenere la posizione GPS esatta e i dati del dispositivo della vittima.",
                "nexphisher": "ℹ️ **INFO NEXPHISHER**: Tool di phishing avanzato per Termux, molto stabile e veloce nell'uso.",
                "pyphisher": "ℹ️ **INFO PYPHISHER**: Strumento Python con 70+ template e sistemi per nascondere i link sospetti."
            }
            text = desc[tool]
            back_btn = types.InlineKeyboardButton("⬅️ TORNA AI COMANDI", callback_data=f"{tool}_cmd")
            markup.add(back_btn)
        elif call.data == "home":
            send_welcome(call.message)
            return
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        print(f"Errore: {e}")

bot.polling()
