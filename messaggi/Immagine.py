from telegram import Update
from telegram.ext import ContextTypes
from messaggi.Messaggio import Messaggio
import openai
import tempfile
import os
import base64

from utenti.Utente import Utente
from Eccezzioni.ParametroEccezione import ParametroEccezione

class Immagine(Messaggio):
    def __init__(self, update: Update, client: openai.OpenAI, utente:Utente, context:ContextTypes.DEFAULT_TYPE):
        super().__init__(update, client, utente, context)

    async def processa(self) -> str:
        user_image = self.update.message.photo[-1]

        file = await self.context.bot.get_file(user_image.file_id)

        with tempfile.TemporaryDirectory() as tmpdir:
            imagejpg = os.path.join(tmpdir, "image.jpg")
            await file.download_to_drive(imagejpg)
            print(imagejpg)

            with open(imagejpg, "rb") as f:
                base64_image = base64.b64encode(f.read()).decode("utf-8")

            image_data_url = f"data:image/jpeg;base64,{base64_image}"

            # Recupera la caption (testo scritto sotto l’immagine)
            caption = self.update.message.caption or "Cosa c'è in questa immagine?"

            message = self.utente.get_storico()
            message.append({  "role": "user",
            "content": [
                {"type": "text", "text": caption},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_data_url,
                    }
                }
            ]})

            try:
                response =self.client.chat.completions.create(
                    model=self.modelgpt,
                    messages= message
                )
                reply = response.choices[0].message.content

                # Aggiunge la domanda del utente allo storico
                self.utente.aggiungi_messaggio("user", caption)
                # Aggiunge la risposta del bot alla cronologia
                self.utente.aggiungi_messaggio("system", reply)

                return reply
            except ParametroEccezione as e:
                print(f"Errore: {e}")
                return "Non supporto questo tipo di dato per contestualizzare il messaggio (solo testo o audio)"
            except Exception as e:
                print(f"Errore: {e}")
                return "⚠️ Errore nel contattare ChatGPT."