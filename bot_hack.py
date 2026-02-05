import telebot
from telebot import types

# Token già inserito
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
    
    bot.reply_to(message, "🔥 **BENVENUTO NEL BOT HACKER** 🔥\nScegli un tool per vedere i comandi:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    markup = types.InlineKeyboardMarkup()
    
    if "_cmd" in call.data:
        tool = call.data.replace("_cmd", "")
        commands = {
            "zphisher": "💻 **COMANDI ZPHISHER**:\n`git clone https://github.com/htr-tech/zphisher` \n`cd zphisher` \n`bash zphisher.sh`",
            "seeker": "💻 **COMANDI SEEKER**:\n`git clone https://github.com/thewhiteh4t/seeker` \n`cd seeker` \n`python3 seeker.py`",
            "nexphisher": "💻 **COMANDI NEXPHISHER**:\n`git clone https://github.com/htr-tech/nexphisher` \n`cd nexphisher` \n`bash nexphisher.sh`",
            "pyphisher": "💻 **COMANDI PYPHISHER**:\n`git clone https://github.com/KasRoudra/PyPhisher` \n`cd PyPhisher` \n`python3 pyphisher.py`"
        }
        text = commands.get(tool, "Errore caricamento.")
        info_btn = types.InlineKeyboardButton("ℹ️ INFORMAZIONI", callback_data=f"{tool}_info")
        back_btn = types.InlineKeyboardButton("⬅️ TORNA AL MENU", callback_data='home')
        markup.add(info_btn, back_btn)

    elif "_info" in call.data:
        tool = call.data.replace("_info", "")
        descriptions = {
            "zphisher": "ℹ️ **COS'È ZPHISHER?**\n\nÈ uno dei tool di phishing più potenti e usati. Permette di creare **pagine web identiche** a quelle dei social (Facebook, Instagram, Google, ecc.) per testare la sicurezza delle password. Include oltre 30 template pronti all'uso e supporta vari sistemi di tunneling.",
            "seeker": "ℹ️ **COS'È SEEKER?**\n\nQuesto strumento viene usato per l'**Ingegneria Sociale**. Invia un link alla vittima che, se cliccato, richiede l'accesso alla posizione. Se accettato, Seeker mostra le **coordinate GPS esatte**, l'altitudine e le informazioni sul dispositivo del bersaglio in tempo reale.",
            "nexphisher": "ℹ️ **COS'È NEXPHISHER?**\n\nÈ una versione evoluta e più stabile di Zphisher. È progettato specificamente per Termux e Linux. Offre template per siti meno comuni ed è molto efficace nel gestire i link che devono superare i controlli di sicurezza dei browser.",
            "pyphisher": "ℹ️ **COS'È PYPHISHER?**\n\nUn tool modernissimo scritto interamente in Python. È incredibile perché offre oltre **77 template diversi** e integra sistemi di mascheramento del link (URL Shortener) per far sembrare il link malevolo del tutto normale e affidabile."
        }
        text = descriptions.get(tool, "Descrizione non disponibile.")
        back_btn = types.InlineKeyboardButton("⬅️ TORNA AI COMANDI", callback_data=f"{tool}_cmd")
        markup.add(back_btn)

    elif call.data == "home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_welcome(call.message)
        return

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")

bot.polling()
