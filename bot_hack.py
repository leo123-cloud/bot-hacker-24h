import telebot
from telebot import types
import datetime
import logging

# --- CONFIGURAZIONE LOGGING (Per rendere il codice professionale) ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CONFIGURAZIONE CORE ---
API_TOKEN = '8461004019:AAHKN207J0ot8LKlc7t8CVhHiQ2xz4t0ua8'
bot = telebot.TeleBot(API_TOKEN)

# --- DATABASE TEMPORANEO ---
TOOLS = {
    "zphisher": {
        "name": "🛡️ ZPHISHER",
        "install": "pkg install git php openssh -y\ngit clone https://github.com/htr-tech/zphisher\ncd zphisher\nbash zphisher.sh",
        "specs": "Framework di phishing automatizzato. Supporta 37 template social e tunneling via Cloudflared.",
        "risk": "Alto - Rilevabile dai browser se non si usa un URL masker."
    },
    "seeker": {
        "name": "📍 SEEKER",
        "install": "pkg install git python php -y\ngit clone https://github.com/thewhiteh4t/seeker\ncd seeker\npython3 seeker.py",
        "specs": "Tool di geolocalizzazione IP/GPS. Estrae coordinate, ISP, e specifiche del device target.",
        "risk": "Medio - Richiede interazione attiva della vittima."
    },
    "nexphisher": {
        "name": "🎣 NEXPHISHER",
        "install": "pkg install git php curl -y\ngit clone https://github.com/htr-tech/nexphisher\ncd nexphisher\nbash nexphisher.sh",
        "specs": "Versione avanzata di phishing con script bash ottimizzati per la velocità su Termux.",
        "risk": "Medio - Molto stabile su reti mobili."
    },
    "pyphisher": {
        "name": "🐍 PYPHISHER",
        "install": "pkg install git python php -y\ngit clone https://github.com/KasRoudra/PyPhisher\ncd PyPhisher\npython3 pyphisher.py",
        "specs": "Suite Python con 77 template. Include sistemi anti-bot per proteggere il link di phishing.",
        "risk": "Basso - Difficile da rilevare grazie ai sistemi di offuscamento."
    }
}

# --- GENERATORE MENU ---
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    row1 = [types.InlineKeyboardButton(TOOLS["zphisher"]["name"], callback_data='zphisher_cmd'),
            types.InlineKeyboardButton(TOOLS["seeker"]["name"], callback_data='seeker_cmd')]
    row2 = [types.InlineKeyboardButton(TOOLS["nexphisher"]["name"], callback_data='nexphisher_cmd'),
            types.InlineKeyboardButton(TOOLS["pyphisher"]["name"], callback_data='pyphisher_cmd')]
    row3 = [types.InlineKeyboardButton("📱 GUIDA TERMUX PRO", callback_data='termux_pro'),
            types.InlineKeyboardButton("🛠️ TOOLS EXTRA", callback_data='extra_tools')]
    markup.add(*row1)
    markup.add(*row2)
    markup.add(*row3)
    return markup

# --- COMANDI PRINCIPALI ---
@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user.first_name
    welcome = (
        f"🚀 **SISTEMA ATTIVO: Benvenuto {user}** 🚀\n"
        "----------------------------------------\n"
        "Accesso alla console Hacker Hub eseguito.\n"
        "Seleziona un'operazione dal menu sottostante.\n"
        "----------------------------------------\n"
        "🕒 " + datetime.datetime.now().strftime("%H:%M:%S")
    )
    bot.send_message(message.chat.id, welcome, reply_markup=main_menu(), parse_mode="Markdown")

# --- GESTIONE CALLBACK (Il cuore del bot) ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:
        # Funzione Torna al Menu con CANCELLAZIONE (Quello che hai chiesto)
        if call.data == "home":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "🔥 **SISTEMA RESETTATO - MENU PRINCIPALE** 🔥", 
                           reply_markup=main_menu(), parse_mode="Markdown")
            return

        # Gestione moduli d'installazione
        for key in TOOLS:
            if call.data == f"{key}_cmd":
                text = (
                    f"💻 **CONSOLE {TOOLS[key]['name']}**\n\n"
                    f"Esegui questi comandi per l'installazione:\n"
                    f"```bash\n{TOOLS[key]['install']}\n```\n"
                    "⚠️ *Assicurati di avere una connessione stabile.*"
                )
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("ℹ️ ANALISI TECNICA", callback_data=f"{key}_info"))
                markup.add(types.InlineKeyboardButton("⬅️ TORNA AL MENU", callback_data="home"))
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                                     reply_markup=markup, parse_mode="Markdown")
                return

            if call.data == f"{key}_info":
                text = (
                    f"ℹ️ **ANALISI TECNICA: {TOOLS[key]['name']}**\n\n"
                    f"🔹 **Descrizione**: {TOOLS[key]['specs']}\n"
                    f"🔸 **Livello Rischio**: {TOOLS[key]['risk']}\n\n"
                    "✅ *Stato del tool: Funzionante*"
                )
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("⬅️ TORNA AI COMANDI", callback_data=f"{key}_cmd"))
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                                     reply_markup=markup, parse_mode="Markdown")
                return

        # Guida Termux Avanzata
        if call.data == "termux_pro":
            text = (
                "📱 **CONFIGURAZIONE TERMUX PROFESSIONALE**\n\n"
                "1️⃣ **Aggiornamento Repository**:\n`pkg update && pkg upgrade -y`\n\n"
                "2️⃣ **Permessi Memoria**:\n`termux-setup-storage`\n\n"
                "3️⃣ **Pacchetti Essenziali**:\n`pkg install git python php curl wget openssh -y`\n\n"
                "4️⃣ **Consiglio**: Usa sempre una VPN per nascondere il tuo IP reale."
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ MENU", callback_data="home"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                                 reply_markup=markup, parse_mode="Markdown")

        # Tools Extra (Per fare massa e utilità)
        if call.data == "extra_tools":
            text = (
                "🛠️ **REPARTI EXTRA - TOOLS AGGIUNTIVI**\n\n"
                "🔹 **SQLMap**: Per database injection.\n"
                "🔹 **Metasploit**: Framework per exploit completi.\n"
                "🔹 **Nmap**: Scansione delle porte di rete.\n\n"
                "Verranno aggiunti nelle prossime versioni del bot."
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ MENU", callback_data="home"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                                 reply_markup=markup, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Errore critico: {e}")
        bot.answer_callback_query(call.id, "Errore nel processare la richiesta.")

# --- AVVIO CONTINUO ---
if __name__ == "__main__":
    logger.info("Bot avviato correttamente.")
    bot.polling(none_stop=True, timeout=60)

# -----------------------------------------------------------------------
# FINE CODICE - Hacker Hub Ultimate Edition
# -----------------------------------------------------------------------
