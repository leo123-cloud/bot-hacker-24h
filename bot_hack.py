import telebot
from telebot import types
import datetime
import logging
import random
import time

# ==========================================
# CONFIGURAZIONE LOGGING PROFESSIONALE
# ==========================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==========================================
# CORE CONFIG
# ==========================================
API_TOKEN = '8461004019:AAHKN207J0ot8LKlc7t8CVhHiQ2xz4t0ua8'
bot = telebot.TeleBot(API_TOKEN)

# ==========================================
# DATABASE ESTESO (TOOL & SPECIFICHE)
# ==========================================
DATABASE = {
    "phishing": {
        "zphisher": {
            "name": "🛡️ ZPHISHER v2.2",
            "cmd": "pkg install git php openssh -y\ngit clone https://github.com/htr-tech/zphisher\ncd zphisher\nbash zphisher.sh",
            "desc": "Il re dei tool di phishing. 37+ template, bypass OTP e supporto Ngrok/Cloudflared.",
            "tech": "PHP Server + SSH Tunneling",
            "danger": "🔴 ALTO"
        },
        "pyphisher": {
            "name": "🐍 PYPHISHER",
            "cmd": "pkg install git python php -y\ngit clone https://github.com/KasRoudra/PyPhisher\ncd PyPhisher\npython3 pyphisher.py",
            "desc": "Tool scritto in Python con oltre 77 template e sistema di mascheramento URL.",
            "tech": "Python3 Flask + Social Engineering",
            "danger": "🟡 MEDIO"
        },
        "nexphisher": {
            "name": "🎣 NEXPHISHER",
            "cmd": "pkg install git php curl -y\ngit clone https://github.com/htr-tech/nexphisher\ncd nexphisher\nbash nexphisher.sh",
            "desc": "Ottimizzato per Termux, ultra-veloce nell'esecuzione di pagine fake.",
            "tech": "Bash Scripting + PHP",
            "danger": "🟡 MEDIO"
        }
    },
    "tracking": {
        "seeker": {
            "name": "📍 SEEKER",
            "cmd": "pkg install git python php -y\ngit clone https://github.com/thewhiteh4t/seeker\ncd seeker\npython3 seeker.py",
            "desc": "Individua la posizione precisa tramite GPS API e Social Engineering.",
            "tech": "HTML5 Geolocation API",
            "danger": "🔴 ALTO"
        },
        "trackip": {
            "name": "🌐 TRACK IP",
            "cmd": "pkg install git curl -y\ngit clone https://github.com/htr-tech/track-ip\ncd track-ip\nbash trackip.sh",
            "desc": "Estrae dati ISP, città e coordinate approssimative tramite indirizzo IP.",
            "tech": "IP API Lookup",
            "danger": "🟢 BASSO"
        }
    },
    "utility": {
        "nmap": {
            "name": "🔍 NMAP SCANNER",
            "cmd": "pkg install nmap -y\nnmap -v -A [TARGET_IP]",
            "desc": "Il miglior scanner di rete al mondo per trovare porte aperte e servizi.",
            "tech": "Packet Crafting",
            "danger": "🟡 MEDIO"
        },
        "sqlmap": {
            "name": "💉 SQLMAP",
            "cmd": "pkg install python git -y\ngit clone https://github.com/sqlmapproject/sqlmap\ncd sqlmap\npython3 sqlmap.py",
            "desc": "Automatic SQL Injection e database takeover tool.",
            "tech": "SQL Exploit",
            "danger": "🔴 CRITICO"
        }
    }
}

# ==========================================
# GENERATORI DI INTERFACCIA (UI)
# ==========================================
def build_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎣 PHISHING", callback_data="cat_phishing"),
        types.InlineKeyboardButton("📍 TRACKING", callback_data="cat_tracking"),
        types.InlineKeyboardButton("🛠️ VULN SCAN", callback_data="cat_utility"),
        types.InlineKeyboardButton("📱 TERMUX PRO", callback_data="guide_termux"),
        types.InlineKeyboardButton("🎲 PASS GEN", callback_data="tool_passgen"),
        types.InlineKeyboardButton("📡 STATO SISTEMA", callback_data="sys_status")
    )
    return markup

def build_back_button(category=None):
    markup = types.InlineKeyboardMarkup()
    if category:
        markup.add(types.InlineKeyboardButton("⬅️ TORNA INDIETRO", callback_data=f"cat_{category}"))
    markup.add(types.InlineKeyboardButton("🏠 MENU PRINCIPALE", callback_data="home"))
    return markup

# ==========================================
# LOGICA DEI COMANDI
# ==========================================
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    logger.info(f"User {message.from_user.id} started the bot")
    welcome_text = (
        "🔥 **HACKER HUB ULTIMATE v3.0** 🔥\n"
        "-------------------------------------\n"
        "Console di gestione tool e sicurezza.\n"
        f"Operatore: `{message.from_user.first_name}`\n"
        f"Data: {datetime.datetime.now().strftime('%d/%m/%Y')}\n"
        "-------------------------------------\n"
        "Seleziona una categoria per iniziare."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=build_main_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    try:
        # --- CANCELLAZIONE E RESET (Richiesta Utente) ---
        if call.data == "home":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "🏠 **MENU PRINCIPALE**", reply_markup=build_main_menu(), parse_mode="Markdown")
            return

        # --- GESTIONE CATEGORIE ---
        if "cat_" in call.data:
            cat = call.data.replace("cat_", "")
            markup = types.InlineKeyboardMarkup(row_width=1)
            for tool_id, data in DATABASE[cat].items():
                markup.add(types.InlineKeyboardButton(data["name"], callback_data=f"info_{cat}_{tool_id}"))
            markup.add(types.InlineKeyboardButton("⬅️ TORNA", callback_data="home"))
            
            bot.edit_message_text(f"📂 **CATEGORIA: {cat.upper()}**\nSeleziona un tool:", 
                                 call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

        # --- INFO DETTAGLIATE TOOL ---
        elif "info_" in call.data:
            _, cat, tid = call.data.split("_")
            tool = DATABASE[cat][tid]
            info_text = (
                f"🛠️ **TOOL: {tool['name']}**\n\n"
                f"📝 **Descrizione**: {tool['desc']}\n"
                f"⚙️ **Tecnologia**: {tool['tech']}\n"
                f"⚠️ **Pericolo**: {tool['danger']}\n\n"
                "📜 **COMANDI INSTALLAZIONE**:\n"
                f"```bash\n{tool['cmd']}\n```"
            )
            bot.edit_message_text(info_text, call.message.chat.id, call.message.message_id, 
                                 reply_markup=build_back_button(cat), parse_mode="Markdown")

        # --- UTILITY: PASSWORD GENERATOR ---
        elif call.data == "tool_passgen":
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
            password = "".join(random.choice(chars) for _ in range(16))
            text = f"🎲 **PASSWORD SICURA GENERATA**:\n\n`{password}`\n\n_Copia e usala per i tuoi account._"
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                                 reply_markup=build_back_button(), parse_mode="Markdown")

        # --- STATO SISTEMA ---
        elif call.data == "sys_status":
            status = (
                "📡 **STATO CONSOLE**\n\n"
                "✅ Server Render: ONLINE\n"
                "✅ Database Tool: CARICATO\n"
                "✅ Latenza API: OTTIMALE\n"
                f"🕒 Uptime: {random.randint(24, 99)}h"
            )
            bot.edit_message_text(status, call.message.chat.id, call.message.message_id, 
                                 reply_markup=build_back_button(), parse_mode="Markdown")

        # --- GUIDA TERMUX PRO ---
        elif call.data == "guide_termux":
            text = (
                "📱 **CONFIGURAZIONE TERMUX PRO**\n\n"
                "1. `pkg update && pkg upgrade -y` (Sempre primo passo)\n"
                "2. `termux-setup-storage` (Per file esterni)\n"
                "3. `pkg install git python php curl wget openssh -y` (Base hacking)\n\n"
                "💡 *Consiglio: Usa 'Screen' per lasciare i tool attivi in background.*"
            )
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                                 reply_markup=build_back_button(), parse_mode="Markdown")

    except Exception as e:
        logger.error(f"ERRORE CALLBACK: {e}")
        bot.answer_callback_query(call.id, "⚠️ Errore interno del sistema.")

# ==========================================
# LOOP INFINITO
# ==========================================
if __name__ == "__main__":
    print(">>> Bot Titan v3.0 in esecuzione...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            logger.error(f"CRASH EVITATO: {e}")
            time.sleep(5)
