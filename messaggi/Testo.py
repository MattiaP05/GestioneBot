from telegram import Update
from telegram.ext import ContextTypes
import openai

from messaggi.Messaggio import Messaggio
from utenti.Utente import Utente
from Eccezzioni.ParametroEccezione import ParametroEccezione

class Testo(Messaggio):
    def __init__(self, update: Update, client: openai.OpenAI, utente:Utente, context:ContextTypes.DEFAULT_TYPE):
        super().__init__(update, client, utente, context)

    async def processa(self) -> str:
        user_message = self.update.message.text

        try:
            response =self.client.chat.completions.create(
                model=self.modelgpt,
                messages=await self.createprompt(user_message)
            )
            reply = response.choices[0].message.content

            # Aggiunge la domanda del utente allo storico
            self.utente.aggiungi_messaggio("user", user_message)
            # Aggiunge la risposta del bot alla cronologia
            self.utente.aggiungi_messaggio("system", reply)

            return reply
        except ParametroEccezione as e:
            print(f"Errore: {e}")
            return "Non supporto questo tipo di dato per contestualizzare il messaggio (solo testo o audio)"
        except Exception as e:
            print(f"Errore: {e}")
            return "⚠️ Errore nel contattare ChatGPT."
