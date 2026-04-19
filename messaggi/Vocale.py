from telegram import Update
from telegram.ext import ContextTypes
import openai

from utenti.Utente import Utente
from messaggi.Messaggio import Messaggio
from Eccezzioni.ParametroEccezione import ParametroEccezione
from Eccezzioni.TrascrizioneEccezione import TrascrizioneEccezione

class Vocale(Messaggio):
    def __init__(self, update: Update, client: openai.OpenAI, utente:Utente, context:ContextTypes.DEFAULT_TYPE):
         super().__init__(update, client, utente, context)
         self.user_message=""

    async def processa(self) -> str:
            try:
                self.user_message = await self.trascrivi(True)

                response =self.client.chat.completions.create(
                    model=self.modelgpt,
                    messages= await self.createprompt(self.user_message)
                )

                reply = response.choices[0].message.content

                # Aggiunge il messaggio dell'utente alla cronologia
                self.utente.aggiungi_messaggio("user", self.user_message)
                # Aggiunge la risposta del bot alla cronologia
                self.utente.aggiungi_messaggio("system", reply)

                return reply

            except ParametroEccezione as e:
                print(f"Errore: {e}")
                return "Non supporto questo tipo di dato per contestualizzare il messaggio (solo testo o audio)"
            except TrascrizioneEccezione as e:
                return "Errore nella comprensione del vocale"
            except Exception as e:
                print(f"Errore: {e}")
                return "⚠️ Errore nel contattare ChatGPT."
