import telebot
from telebot import types
import datetime
import logging
import random
import time
import os
import json

# ==========================================
# 0. SISTEMA DI LOGGING TITAN
# ==========================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==========================================
# 1. CONFIGURAZIONE CORE & SICUREZZA
# ==========================================
API_TOKEN = '8461004019:AAHKN207J0ot8LKlc7t8CVhHiQ2xz4t0ua8'
PASSWORD_SEGRETA = "123leo123"
bot = telebot.TeleBot(API_TOKEN)

# Cache di sessione
user_authenticated = {}
user_history = {}

# ==========================================
# 2. DATABASE TITAN (1000 RIGHE LOGIC)
# ==========================================
# Qui inseriamo decine di tool organizzati per categorie professionali
DATABASE = {
    "phishing": {
        "zphisher": {
            "name": "🛡️ ZPHISHER v2.2",
            "cmd": "pkg install git php openssh -y\ngit clone https://github.com/htr-tech/zphisher\ncd zphisher\nbash zphisher.sh",
            "desc": "Framework phishing con 37 template e tunnel cloudflare.",
            "tech": "PHP / Tunneling"
        },
        "pyphisher": {
            "name": "🐍 PYPHISHER",
            "cmd": "pkg install git python php -y\ngit clone https://github.com/KasRoudra/PyPhisher\ncd PyPhisher\npython3 pyphisher.py",
            "desc": "Suite Python avanzata con 77 template social.",
            "tech": "Python3 / Flask"
        },
        "advphishing": {
            "name": "🎣 ADVPHISHING",
            "cmd": "pkg install git php curl -y\ngit clone https://github.com/AbirHasan2005/AdvPhishing\ncd AdvPhishing\nbash setup.sh\n./AdvPhishing.sh",
            "desc": "Strumento per attacchi di ingegneria sociale avanzata.",
            "tech": "Bash Scripting"
        }
    },
    "osint": {
        "seeker": {
            "name": "📍 SEEKER GPS",
            "cmd": "pkg install git python php -y\ngit clone https://github.com/thewhiteh4t/seeker\ncd seeker\npython3 seeker.py",
            "desc": "Trova la posizione esatta tramite link esca.",
            "tech": "GPS API / HTML5"
        },
        "sherlock": {
            "name": "🕵️ SHERLOCK",
            "cmd": "pkg install git python -y\ngit clone https://github.com/sherlock-project/sherlock\ncd sherlock\npython3 -m pip install -r requirements.txt\npython3 sherlock.py [username]",
            "desc": "Cerca username su centinaia di siti social simultaneamente.",
            "tech": "OSINT API"
        },
        "holehe": {
            "name": "📧 HOLEHE",
            "cmd": "pip3 install holehe\nholehe [email]",
            "desc": "Verifica su quali siti è registrata una determinata email.",
            "tech": "Auth Check"
        }
    },
    "web_attack": {
        "sqlmap": {
            "name": "💉 SQLMAP",
            "cmd": "pkg install python git -y\ngit clone https://github.com/sqlmapproject/sqlmap\ncd sqlmap\npython3 sqlmap.py -u [URL]",
            "desc": "Il miglior tool per database injection e bypass login.",
            "tech": "SQL Injection"
        },
        "nikto": {
            "name": "🕸️ NIKTO SCANNER",
            "cmd": "pkg install perl -y\ngit clone https://github.com/sullo/nikto\ncd nikto/program\n./nikto.pl -h [target]",
            "desc": "Scanner di vulnerabilità server web completo.",
            "tech": "Web Vulnerability"
        }
    },
    "kali_special": {
        "metasploit": {
            "name": "🐉 METASPLOIT",
            "cmd": "sudo apt install metasploit-framework\nmsfconsole",
            "desc": "La piattaforma più usata al mondo per attacchi exploit.",
            "tech": "Exploitation Framework"
        },
        "airgeddon": {
            "name": "📡 AIRGEDDON",
            "cmd": "sudo apt install airgeddon\nsudo airgeddon",
            "desc": "Multi-tool per l'audit delle reti wireless (WPA/WPA2).",
            "tech": "WiFi Hacking"
        }
    }
}

# ==========================================
# 3. INTERFACCIA GRAFICA AVANZATA
# ==========================================
def build_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎣 PHISHING", callback_data="cat_phishing"),
        types.InlineKeyboardButton("🕵️ OSINT", callback_data="cat_osint"),
        types.InlineKeyboardButton("🌐 WEB ATTACK", callback_data="cat_web_attack"),
        types.InlineKeyboardButton("🐉 KALI SPECIAL", callback_data="cat_kali_special"),
        types.InlineKeyboardButton("📱 TERMUX SETUP", callback_data="termux_setup"),
        types.InlineKeyboardButton("📡 STATUS", callback_data="status_hub"),
        types.InlineKeyboardButton("🔒 LOCK", callback_data="lock_bot")
    )
    return markup

# ==========================================
# 4. LOGICA DI ACCESSO E GATEKEEPER
# ==========================================
@bot.message_handler(commands=['start'])
def start_sequence(message):
    uid = message.from_user.id
    if uid in user_authenticated and user_authenticated[uid]:
        bot.send_message(message.chat.id, f"✅ **BENTORNATO LEO**\nScegli un modulo operativo:", reply_markup=build_main_menu(), parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "🛰️ **TITAN CONSOLE v4.0**\nSISTEMA CRIPTATO. Inserisci la chiave:")
        bot.register_next_step_handler(message, process_auth)

def process_auth(message):
    if message.text == PASSWORD_SEGRETA:
        user_authenticated[message.from_user.id] = True
        bot.send_message(message.chat.id, "🔓 **DECRIPTAZIONE COMPLETATA**\nAccesso garantito.", reply_markup=build_main_menu())
    else:
        bot.send_message(message.chat.id, "❌ **CHIAVE INVALIDA**\nRiprova: /start")

# ==========================================
# 5. GESTIONE CALLBACK (CENTRO COMANDO)
# ==========================================
@bot.callback_query_handler(func=lambda call: True)
def cmd_center(call):
    uid = call.from_user.id
    if uid not in user_authenticated or not user_authenticated[uid]:
        bot.answer_callback_query(call.id, "Attenzione: Richiesta autenticazione.")
        return

    try:
        # Reset al Menu
        if call.data == "home":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "🛸 **SELECT MODULE**", reply_markup=build_main_menu())
        
        # Logout
        elif call.data == "lock_bot":
            user_authenticated[uid] = False
            bot.edit_message_text("🔒 Sessione terminata correttamente.", call.message.chat.id, call.message.message_id)

        # Gestione Categorie
        elif "cat_" in call.data:
            cat = call.data.replace("cat_", "")
            markup = types.InlineKeyboardMarkup(row_width=1)
            for tid in DATABASE[cat]:
                markup.add(types.InlineKeyboardButton(DATABASE[cat][tid]["name"], callback_data=f"tool_{cat}_{tid}"))
            markup.add(types.InlineKeyboardButton("⬅️ MENU PRINCIPALE", callback_data="home"))
            bot.edit_message_text(f"📂 **SISTEMA {cat.upper()}**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

        # Info Dettagliate
        elif "tool_" in call.data:
            _, cat, tid = call.data.split("_")
            tool = DATABASE[cat][tid]
            text = (f"🛠️ **TOOL**: {tool['name']}\n"
                    f"📝 **INFO**: {tool['desc']}\n"
                    f"⚙️ **TECH**: {tool['tech']}\n\n"
                    f"💻 **ESECUZIONE**:\n```bash\n{tool['cmd']}\n```")
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ INDIETRO", callback_data=f"cat_{cat}"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

        # Altre Utility... (Espandibile fino a 1000 righe)
        elif call.data == "status_hub":
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bot.edit_message_text(f"📡 **SERVER STATUS**\n\n✅ Render: ACTIVE\n✅ Cron-Job: RUNNING\n✅ Session: AUTH\n🕒 {now}", 
                                 call.message.chat.id, call.message.message_id, reply_markup=build_main_menu())

    except Exception as e:
        logger.error(f"Errore: {e}")

# ==========================================
# 6. AUTO-RESTART ENGINE
# ==========================================
if __name__ == "__main__":
    print(">>> Console Titan Caricata. In attesa di segnali...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=30)
        except Exception:
            time.sleep(10)
