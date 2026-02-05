import telebot
from telebot import types
import time

# CONFIGURAZIONE CORE
API_TOKEN = '8461004019:AAHKN207J0ot8LKlc7t8CVhHiQ2xz4t0ua8'
bot = telebot.TeleBot(API_TOKEN)

# --- FUNZIONI DI SUPPORTO ---
def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛡️ ZPHISHER", callback_data='zphisher_cmd'),
        types.InlineKeyboardButton("📍 SEEKER", callback_data='seeker_cmd'),
        types.InlineKeyboardButton("🎣 NEXPHISHER", callback_data='nexphisher_cmd'),
        types.InlineKeyboardButton("🐍 PYPHISHER", callback_data='pyphisher_cmd'),
        types.InlineKeyboardButton("📱 GUIDA TERMUX", callback_data='termux_guide'),
        types.InlineKeyboardButton("⚖️ DISCLAIMER", callback_data='legal_info')
    ]
    markup.add(*buttons)
    return markup

# --- GESTIONE COMANDI ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🛠️ **HACKER CONSOLE v2.0 - ULTIMATE** 🛠️\n"
        "--------------------------------------\n"
        "Benvenuto operatore. Il sistema è pronto.\n"
        "Seleziona un modulo per visualizzare comandi e specifiche."
    )
    bot.reply_to(message, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        # CANCELLAZIONE MESSAGGIO PER PULIZIA (Quello che hai chiesto)
        if call.data == "home":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "🔥 **MENU PRINCIPALE** 🔥", reply_markup=get_main_menu(), parse_mode="Markdown")
            return

        # LOGICA TOOL (COMANDI)
        if "_cmd" in call.data:
            tool = call.data.replace("_cmd", "")
            cmds = {
                "zphisher": "pkg install git php openssh -y\ngit clone https://github.com/htr-tech/zphisher\ncd zphisher\nbash zphisher.sh",
                "seeker": "pkg install git python php -y\ngit clone https://github.com/thewhiteh4t/seeker\ncd seeker\npython3 seeker.py",
                "nexphisher": "pkg install git php curl -y\ngit clone https://github.com/htr-tech/nexphisher\ncd nexphisher\nbash nexphisher.sh",
                "pyphisher": "pkg install git python php -y\ngit clone https://github.com/KasRoudra/PyPhisher\ncd PyPhisher\npython3 pyphisher.py"
            }
            
            text = f"💻 **COMANDI INSTALLAZIONE {tool.upper()}**\n\n```bash\n{cmds[tool]}\n```\n\n_Copia e incolla nel tuo terminale._"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("ℹ️ SPECIFICHE TECNICHE", callback_data=f"{tool}_info"))
            markup.add(types.InlineKeyboardButton("⬅️ TORNA AL MENU", callback_data='home'))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

        # SPECIFICHE TECNICHE (Descrizioni lunghe e professionali)
        elif "_info" in call.data:
            tool = call.data.replace("_info", "")
            info_data = {
                "zphisher": "🛡️ **ZPHISHER - SPECIFICHE AVANZATE**\n\n- **Type**: Automated Social Engineering Framework.\n- **Tunneling**: Supporta Cloudflared e Ngrok per bypassare i firewall ISP.\n- **Payload**: Pagine HTML5 responsive che imitano perfettamente i login di Facebook, Instagram e Google.\n- **Database**: Memorizza IP, User-Agent e credenziali in file .txt locali.",
                "seeker": "📍 **SEEKER - SPECIFICHE AVANZATE**\n\n- **Type**: Geolocation Tracker.\n- **Exploit**: Sfrutta le API HTML5 Geolocation tramite permessi browser.\n- **Data Leak**: Restituisce Latitudine, Longitudine, Altitudine, Velocità e informazioni dettagliate sulla batteria del dispositivo.\n- **Uso**: Ottimo per OSINT e rintracciamento bersagli fisici.",
                "nexphisher": "🎣 **NEXPHISHER - SPECIFICHE AVANZATE**\n\n- **Type**: Advanced Phishing Kit.\n- **Bypass**: Script ottimizzato per evitare la segnalazione di 'Sito Pericoloso' su Chrome e Safari.\n- **Interfaccia**: Menu CLI semplificato per attacchi rapidi su reti locali e remote.",
                "pyphisher": "🐍 **PYPHISHER - SPECIFICHE AVANZATE**\n\n- **Type**: Python Phishing Suite.\n- **Template**: 77 pagine di phishing (il numero più alto della categoria).\n- **Sicurezza**: Include un sistema di mascheramento URL integrato (Url shortener) per nascondere l'indirizzo sospetto."
            }
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ TORNA AI COMANDI", callback_data=f"{tool}_cmd"))
            bot.edit_message_text(info_data[tool], call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

        # GUIDA TERMUX
        elif call.data == "termux_guide":
            guide = (
                "📱 **GUIDA TERMUX PER PRINCIPIANTI**\n\n"
                "1. Scarica Termux da F-Droid (non dal Play Store).\n"
                "2. Esegui `pkg update && pkg upgrade` appena lo apri.\n"
                "3. Consenti l'archiviazione con `termux-setup-storage`.\n"
                "4. Ora puoi installare i tool del menu!"
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ MENU", callback_data='home'))
            bot.edit_message_text(guide, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

        # DISCLAIMER LEGALE
        elif call.data == "legal_info":
            legal = (
                "⚖️ **AVVISO LEGALE**\n\n"
                "Questo bot è stato creato esclusivamente a scopo **educativo e di ricerca sulla sicurezza informativa**.\n\n"
                "L'uso di questi strumenti contro obiettivi senza autorizzazione è illegale. L'autore non si assume alcuna responsabilità per l'uso improprio."
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ MENU", callback_data='home'))
            bot.edit_message_text(legal, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    except Exception as e:
        print(f"Errore rilevato: {e}")

bot.polling(none_stop=True)
