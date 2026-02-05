import telebot
from telebot import types

# CONFIGURAZIONE
API_TOKEN = '8461004019:AAHKN207J0ot8LKlc7t8CVhHiQ2xz4t0ua8'
bot = telebot.TeleBot(API_TOKEN)

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🛡️ ZPHISHER", callback_data='zphisher_cmd')
    btn2 = types.InlineKeyboardButton("📍 SEEKER", callback_data='seeker_cmd')
    btn3 = types.InlineKeyboardButton("🎣 NEXPHISHER", callback_data='nexphisher_cmd')
    btn4 = types.InlineKeyboardButton("🐍 PYPHISHER", callback_data='pyphisher_cmd')
    btn5 = types.InlineKeyboardButton("📱 GUIDA TERMUX", callback_data='termux_guide')
    btn6 = types.InlineKeyboardButton("⚖️ DISCLAIMER", callback_data='legal_info')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🛠️ **HACKER CONSOLE v2.0** 🛠️\nSeleziona un modulo:", reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        # LOGICA CANCELLAZIONE E TORNA AL MENU
        if call.data == "home":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "🔥 **MENU PRINCIPALE** 🔥", reply_markup=get_main_menu(), parse_mode="Markdown")
            return

        # DISCLAIMER (Sistemato)
        if call.data == "legal_info":
            legal_text = "⚖️ **AVVISO LEGALE**\n\nQuesto tool è a solo scopo educativo. L'uso improprio è punibile dalla legge. L'autore non è responsabile delle tue azioni."
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ MENU", callback_data='home'))
            bot.edit_message_text(legal_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            return

        # GUIDA TERMUX
        if call.data == "termux_guide":
            guide_text = "📱 **GUIDA TERMUX**\n1. Installa da F-Droid\n2. `pkg update && pkg upgrade`\n3. Installa i tool dal menu."
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ MENU", callback_data='home'))
            bot.edit_message_text(guide_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            return

        # COMANDI TOOL
        if "_cmd" in call.data:
            tool = call.data.replace("_cmd", "")
            cmds = {
                "zphisher": "pkg install git php -y\ngit clone https://github.com/htr-tech/zphisher\ncd zphisher\nbash zphisher.sh",
                "seeker": "pkg install git python -y\ngit clone https://github.com/thewhiteh4t/seeker\ncd seeker\npython3 seeker.py",
                "nexphisher": "pkg install git php -y\ngit clone https://github.com/htr-tech/nexphisher\ncd nexphisher\nbash nexphisher.sh",
                "pyphisher": "pkg install git python -y\ngit clone https://github.com/KasRoudra/PyPhisher\ncd PyPhisher\npython3 pyphisher.py"
            }
            text = f"💻 **INSTALLA {tool.upper()}**\n\n```bash\n{cmds[tool]}\n```"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("ℹ️ INFO", callback_data=f"{tool}_info"))
            markup.add(types.InlineKeyboardButton("⬅️ MENU", callback_data='home'))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

        # INFO TOOL
        elif "_info" in call.data:
            tool = call.data.replace("_info", "")
            descriptions = {
                "zphisher": "🛡️ **ZPHISHER**: Framework di phishing con 30+ template. Usa il tunneling per creare link esterni.",
                "seeker": "📍 **SEEKER**: Individua la posizione GPS precisa sfruttando le API del browser della vittima.",
                "nexphisher": "🎣 **NEXPHISHER**: Tool veloce per Termux, specializzato in attacchi social rapidi.",
                "pyphisher": "🐍 **PYPHISHER**: Il più completo, con 77 pagine e mascheramento link avanzato."
            }
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ COMANDI", callback_data=f"{tool}_cmd"))
            bot.edit_message_text(descriptions[tool], call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    except Exception as e:
        print(f"Errore: {e}")

bot.polling(none_stop=True)
