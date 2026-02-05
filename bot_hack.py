import telebot
from telebot import types

API_TOKEN = '8461004019:AAHKN207J0ot8LKlc7t8CVhHiQ2xz4t0ua8'
bot = telebot.TeleBot(API_TOKEN)

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🛡️ Zphisher", callback_data='zphisher_cmd')
    btn2 = types.InlineKeyboardButton("📍 Seeker", callback_data='seeker_cmd')
    btn3 = types.InlineKeyboardButton("🎣 Nexphisher", callback_data='nexphisher_cmd')
    btn4 = types.InlineKeyboardButton("🐍 PyPhisher", callback_data='pyphisher_cmd')
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔥 **HACKER HUB - ELITE CONSOLE** 🔥\nScegli un modulo d'attacco per iniziare:", reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        # Se l'utente preme "Torna al Menu", cancelliamo il messaggio corrente e ne mandiamo uno nuovo
        if call.data == "home":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id, "🔥 **HACKER HUB - ELITE CONSOLE** 🔥\nScegli un modulo d'attacco:", reply_markup=get_main_menu(), parse_mode="Markdown")
            return

        markup = types.InlineKeyboardMarkup()
        
        if "_cmd" in call.data:
            tool = call.data.replace("_cmd", "")
            cmds = {
                "zphisher": "`git clone https://github.com/htr-tech/zphisher` \n`cd zphisher` \n`bash zphisher.sh`",
                "seeker": "`git clone https://github.com/thewhiteh4t/seeker` \n`cd seeker` \n`python3 seeker.py`",
                "nexphisher": "`git clone https://github.com/htr-tech/nexphisher` \n`cd nexphisher` \n`bash nexphisher.sh`",
                "pyphisher": "`git clone https://github.com/KasRoudra/PyPhisher` \n`cd PyPhisher` \n`python3 pyphisher.py`"
            }
            text = f"💻 **MODULO DI INSTALLAZIONE: {tool.upper()}**\n\nCopia ed esegui i comandi sul terminale:\n{cmds[tool]}"
            info_btn = types.InlineKeyboardButton("ℹ️ SPECIFICHE TECNICHE", callback_data=f"{tool}_info")
            back_btn = types.InlineKeyboardButton("⬅️ TORNA AL MENU", callback_data='home')
            markup.add(info_btn, back_btn)

        elif "_info" in call.data:
            tool = call.data.replace("_info", "")
            desc = {
                "zphisher": "🛡️ **SPECIFICHE ZPHISHER**\n\n* **Attacco**: Automated Phishing Framework.\n* **Tecnica**: Sfrutta il port forwarding (Cloudflared/Ngrok) per esporre server locali.\n* **Target**: Credenziali Social, Email, Cloud.\n* **Note**: Include 37 template con bypass dei filtri spam.",
                "seeker": "📍 **SPECIFICHE SEEKER**\n\n* **Attacco**: Social Engineering Location Tracking.\n* **Tecnica**: Triangolazione GPS tramite API del browser.\n* **Dati estratti**: Latitudine, Longitudine, Altitudine, Precisione, ISP e OS del device.\n* **Note**: Richiede l'interazione della vittima su un link esca.",
                "nexphisher": "🎣 **SPECIFICHE NEXPHISHER**\n\n* **Attacco**: High-Speed Phishing Tool.\n* **Tecnica**: Ottimizzato per Termux con script bash ad alta efficienza.\n* **Target**: Portali di login moderni.\n* **Note**: Ideale per attacchi rapidi in mobilità.",
                "pyphisher": "🐍 **SPECIFICHE PYPHISHER**\n\n* **Attacco**: Multi-Platform Phishing Hub.\n* **Tecnica**: Scritto in Python con 77 template pre-caricati.\n* **Funzioni**: Mascheramento URL integrato e rilevamento bot di sicurezza.\n* **Note**: Il tool più completo per diversificazione di attacco."
            }
            text = desc[tool]
            back_btn = types.InlineKeyboardButton("⬅️ TORNA AI COMANDI", callback_data=f"{tool}_cmd")
            markup.add(back_btn)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=markup, parse_mode="Markdown")
            
    except Exception as e:
        print(f"Errore: {e}")

bot.polling()
