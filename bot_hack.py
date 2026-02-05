import telebot
from telebot import types

# Inserisci qui il tuo TOKEN di BotFather
API_TOKEN = 'IL_TUO_TOKEN_QUI'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🛡️ Zphisher", callback_data='zphisher_cmd')
    btn2 = types.InlineKeyboardButton("📍 Seeker", callback_data='seeker_cmd')
    btn3 = types.InlineKeyboardButton("🎣 Nexphisher", callback_data='nexphisher_cmd')
    btn4 = types.InlineKeyboardButton("🐍 PyPhisher", callback_data='pyphisher_cmd')
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.reply_to(message, "🔥 **BENVENUTO NEL BOT HACKER** 🔥\nScegli un tool per vedere i comandi di installazione:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    markup = types.InlineKeyboardMarkup()
    
    # Gestione COMANDI
    if "_cmd" in call.data:
        tool = call.data.replace("_cmd", "")
        if tool == "zphisher":
            text = "💻 **COMANDI ZPHISHER**:\n`git clone https://github.com/htr-tech/zphisher` \n`cd zphisher` \n`bash zphisher.sh`"
        elif tool == "seeker":
            text = "💻 **COMANDI SEEKER**:\n`git clone https://github.com/thewhiteh4t/seeker` \n`cd seeker` \n`python3 seeker.py`"
        elif tool == "nexphisher":
            text = "💻 **COMANDI NEXPHISHER**:\n`git clone https://github.com/htr-tech/nexphisher` \n`cd nexphisher` \n`bash nexphisher.sh`"
        elif tool == "pyphisher":
            text = "💻 **COMANDI PYPHISHER**:\n`git clone https://github.com/KasRoudra/PyPhisher` \n`cd PyPhisher` \n`python3 pyphisher.py`"
        
        info_btn = types.InlineKeyboardButton("ℹ️ INFORMAZIONI", callback_data=f"{tool}_info")
        back_btn = types.InlineKeyboardButton("⬅️ TORNA AL MENU", callback_data='home')
        markup.add(info_btn)
        markup.add(back_btn)

    # Gestione INFORMAZIONI
    elif "_info" in call.data:
        tool = call.data.replace("_info", "")
        if tool == "zphisher":
            text = "ℹ️ **INFO ZPHISHER**:\nTool di phishing con oltre 30 template pronti per social e siti web."
        elif tool == "seeker":
            text = "ℹ️ **INFO SEEKER**:\nTrova la posizione esatta (GPS) del bersaglio tramite un semplice link."
        elif tool == "nexphisher":
            text = "ℹ️ **INFO NEXPHISHER**:\nVersione migliorata di Zphisher con supporto per tunneling avanzati."
        elif tool == "pyphisher":
            text = "ℹ️ **INFO PYPHISHER**:\nPotente tool in Python con 70+ template e mascheramento link."
        
        back_btn = types.InlineKeyboardButton("⬅️ TORNA AI COMANDI", callback_data=f"{tool}_cmd")
        markup.add(back_btn)

    # Torna alla Home
    elif call.data == "home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message)
        return

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

bot.polling()
