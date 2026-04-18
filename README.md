## GestioneBot 🤖

Un bot Telegram intelligente che trasforma la tua chat in un'esperienza conversazionale avanzata. Grazie all'integrazione con le API di OpenAI, il bot non si limita a rispondere, ma interagisce in tempo reale con testo, immagini e messaggi vocali, offrendo risposte naturali e fluide.


Tutte le chat vengono salvate nella cartella utenti/json/ tramite file JSON. Ogni file è nominato con l'ID dell'utente a cui appartiene la conversazione.

## Funzionalità
- Conversazione Naturale
- Trascrizione Vocale di Precisione
- Interpretazione Multimodale
- Salvataggio delle chat

## Guida all'installazione e configurazione del bot Telegram.

📋 Requisiti

Python 3.x
pip
Un account Telegram con un bot creato tramite BotFather


🚀 Installazione
1. Clona il repository
bashgit clone https://github.com/MattiaP05/GestioneBot
cd GestioneBot
2. Installa le dipendenze Python
bashpip install pipreqs
pipreqs . --force
pip install -r requirements.txt
3. Genera le chiavi di sicurezza
bashcd Sicurezza
python generate_key.py
4. Inserisci le tue API
Apri il file encrypt_tokens.py e inserisci le tue API Telegram (quelle generate con BotFather), poi esegui:
bashpython encrypt_tokens.py
5. Avvia il Bot
bashpython Main.py

📁 Struttura del progetto
GestioneBot/
├── Sicurezza/
│   ├── generate_key.py
│   └── encrypt_tokens.py
├── Main.py
└── requirements.txt
    python Main.py