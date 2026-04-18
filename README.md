# Gestione Bot

Un bot Telegram intelligente che trasforma la tua chat in un'esperienza conversazionale avanzata. Grazie all'integrazione con le API di OpenAI, il bot non si limita a rispondere, ma interagisce in tempo reale con testo, immagini e messaggi vocali, offrendo risposte naturali e fluide.


Tutte le chat vengono salvate nella cartella utenti/json/ tramite file JSON. Ogni file è nominato con l'ID dell'utente a cui appartiene la conversazione.

## Funzionalità
- Conversazione Naturale
- Trascrizione Vocale di Precisione
- Interpretazione Multimodale
- Salvataggio delle chat

## Come installarlo
1. Clona il repository:
   git clone https://github.com/MattiaP05/GestioneBot

2. Installazione dipendenze Python con pipreqs
    pip install pipreqs
    pipreqs . --force
    pip install -r requirements.txt
3. Generare le chiavi
    cd Sicurezza
    python generate_key.py
4.  Inserire Le proprie API
    Modifica il file encrypt_tokens.py inserendo le API telegram(Quelle di generate con BotFather) in telegram_token e le API di OpenIA in openai_key.
    Esegui python  encrypt_tokens.py
5. Eseguire il Bot
    python Main.py