from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes
import openai
import tempfile
import ffmpeg
import whisper
import os
import torch

from utenti.Utente import Utente
from Eccezzioni.ParametroEccezione import ParametroEccezione
from Eccezzioni.TrascrizioneEccezione import TrascrizioneEccezione

# Classe astratta Messaggio
class Messaggio(ABC):
    def __init__(self, update: Update, openai_client: openai.OpenAI, utente: Utente,  context:ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.client = openai_client
        self.utente = utente
        self.modelgpt = "gpt-4o" #LLM che si vuole usare di OpenIA
        self.context = context

    @abstractmethod
    async def processa(self) -> list:
        pass  # Metodo astratto, va implementato nelle sottoclassi

    async def createprompt(self, user_message: str):
        messages = [{"role": "system", "content": "Sei un bot Telegram che risponde con messaggi brevi, chiari e diretti. I messaggi ricevuti dagli utenti possono essere scollegati tra loro. Non fare domande a meno che non sia assolutamente necessario. Non usare frasi lunghe o troppo formali. Rispondi in modo utile, conciso e amichevole."}]
        messages += self.utente.get_storico()  # storico passato

        if (self.update.message.reply_to_message is not None):  # risposta ad un messaggio specifico
            if(self.update.message.reply_to_message.voice is not None):
                messages.append({"role": "system",
                                 "content": "Messaggio scritto in precedenza, l'utente si sta riferendo a questo nel messaggio sucessivo: " + await self.trascrivi(False)})
                messages.append({"role": "user", "content": user_message})
            elif(self.update.message.reply_to_message.text is not None):
                messages.append({"role": "system",
                                 "content": "Messaggio scritto in precedenza, l'utente si sta riferendo a questo nel messaggio sucessivo: " + self.update.message.reply_to_message.text})
                messages.append({"role": "user", "content": user_message})
            else:
                messages.append({"role": "user", "content": "Ho commesso un ERRORE, NON RISPONDERE"})
                raise ParametroEccezione("Contestualizzazione non supportata")
        else:
            messages.append({"role": "user", "content": user_message})  # nuovo input utente

        print(messages)
        print(self.update.message.from_user)

        return messages

    async def trascrivi(self, tipo: bool) -> str:
        if tipo:#Il messaggio è un vocale
            voice=self.update.message.voice
        else:#Il contensto del messaggio è un vocale
            voice=self.update.message.reply_to_message.voice

        file = await self.context.bot.get_file(voice.file_id)

        with tempfile.TemporaryDirectory() as tmpdir:
            ogg_path = os.path.join(tmpdir, "audio.ogg")
            wav_path = os.path.join(tmpdir, "audio.wav")
            print(ogg_path)
            print(wav_path)

            await file.download_to_drive(ogg_path)

            try:
                # Converti .ogg in .wav con ffmpeg
                ffmpeg.input(ogg_path).output(wav_path).run(quiet=True, overwrite_output=True, capture_stderr=True)

                model = whisper.load_model("base", device="cuda" if torch.cuda.is_available() else "cpu")
                transcript = model.transcribe(wav_path, fp16=False)#Imposta fp16=True se si possiete tanta VRAM

                user_message = transcript["text"]
                return user_message
            except ffmpeg.Error as e:
                print(f"Errore durante la conversione: {e.stderr.decode()}")
                raise TrascrizioneEccezione("Errore durante la conversione da ogg a wav")
            except Exception as e:
                print(f"Errore vocale: {e}")
                raise TrascrizioneEccezione("Errore durante la trascrizione da audio a testo")