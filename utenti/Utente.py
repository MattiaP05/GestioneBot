import json
import os

percorso = os.getcwd() + "/utenti/json/"

class Utente:
    def __init__(self, user_id):
        self.user_id = user_id
        if (self.is_file_empty(percorso + "dati" + str(self.user_id) + ".json")):
            with open(percorso + "dati" + str(self.user_id) + ".json", "w") as file:
                json.dump([{"role": "system", "content": "Inizio la conversazione con " + str(
                    user_id) + ". Non ho scritto io questo messaggio, è di default"}], file, indent=4)
        self.conversazione = self.load()

    def aggiungi_messaggio(self, ruolo, contenuto) -> None:
        self.conversazione.append({"role": ruolo, "content": contenuto})
        self.stored()

    def get_storico(self) -> list:
        return self.conversazione[-10:]  # ultimi 10 messaggi

    def stored(self) -> None:
        with open(percorso + "dati" + str(self.user_id) + ".json", "w") as file:
            json.dump(self.conversazione, file, indent=4)

    def load(self) -> list:
        with open(percorso + "dati" + str(self.user_id) + ".json", "r") as file:
            conversazione = json.load(file)
        return conversazione

    def is_file_empty(self, filepath) -> bool:
        try:
            with open(filepath, 'r') as f:
                # Controlla se il file è vuoto leggendo il primo carattere
                if f.read(1) == '':
                    return True
                else:
                    return False
        except FileNotFoundError:
            # Se il file non esiste, lo considera vuoto
            return True