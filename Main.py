from cryptography.fernet import Fernet
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from utenti.Utente import Utente
from messaggi.Testo import Testo
from messaggi.Immagine import Immagine
from messaggi.Vocale import Vocale

# === CONFIGURAZIONE ===

# Carica la chiave
with open("Sicurezza/fernet.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Legge e decifra i token
with open("Sicurezza/telegram_token.txt", "rb") as f:
    TELEGRAM_TOKEN = fernet.decrypt(f.read()).decode()

with open("Sicurezza/openai_key.txt", "rb") as f:
    OPENAI_API_KEY = fernet.decrypt(f.read()).decode()

# === CLIENT OPENAI ===
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# === Gestione utenti ===
utenti = {}  # Dizionario {user_id: Utente}

def InizializzaUtente(user_id) -> None:
    # Crea un nuovo oggetto Utente se non esiste
    if user_id not in utenti:
        utenti[user_id] = Utente(user_id)


# === FUNZIONE /start. Passa i link iniziali. Questo è un comando d'esempio===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("Messaggi_Comandi/start.txt", "r") as start:
        messaggio = start.read()
    await update.message.reply_text(messaggio)

    user_id = update.effective_user.id  # id del utente

    InizializzaUtente(user_id)
    utente = utenti[user_id]

    # Aggiunge il messaggio dell'utente alla cronologia
    utente.aggiungi_messaggio("user", messaggio)

# === Handler per messaggi testuali ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id  # id del utente
    InizializzaUtente(user_id)
    utente = utenti[user_id]

    try:
        testo = Testo(update, client, utente, context)
        risposta= await testo.processa()
        await update.message.reply_text(risposta)
    except Exception as e:
        await update.message.reply_text("Problemi nel contattare il server, riprovare")
        print(f"Errore: {e}")

# === Handler per messaggi vocali ===
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id  # id del utente
    InizializzaUtente(user_id)
    utente = utenti[user_id]

    try:
        vocale = Vocale(update, client, utente, context)
        risposta= await vocale.processa()
        await update.message.reply_text("Hai detto: " + vocale.user_message)
        await update.message.reply_text(risposta)
    except Exception as e:
        await update.message.reply_text("Problemi nel contattare il server, riprovare")
        print(f"Errore: {e}")

# === Handler per le immagini ===
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id  # id del utente
    InizializzaUtente(user_id)
    utente = utenti[user_id]
    try:
        immagine = Immagine(update, client, utente, context)
        risposta = await immagine.processa()
        await update.message.reply_text(risposta)
    except Exception as e:
        await update.message.reply_text("Problemi nel contattare il server, riprovare")
        print(f"Errore: {e}")

def main():
    logging.basicConfig(level=logging.INFO)
    try:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_handler(MessageHandler(filters.VOICE, handle_voice))
        app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

        print("🤖 Bot avviato!")
        app.run_polling(timeout=30)
    except Exception as e:
        print(f"Errore: {e}")

# === AVVIO DEL BOT ===
if __name__ == '__main__':
   main()