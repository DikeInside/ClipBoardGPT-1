# Importa le classi necessarie da Tkinter e gli altri moduli richiesti
from tkinter import Tk, Canvas, simpledialog, Button, StringVar, OptionMenu
import pyperclip
import requests
import threading
import time
import datetime

# Classe principale dell'applicazione ClipboardGPT
class ClipboardGPTApp:
    def __init__(self, root):
        # Inizializzazione delle variabili principali
        self.root = root  # Finestra principale dell'applicazione
        self.api_key = ""  # Chiave API per OpenAI
        self.model = "gpt-3.5-turbo"  # Modello AI predefinito
        self.prefix = ""  # Prefisso per i comandi
        self.active = False  # Indica se l'app è attiva
        self.logging_enabled = False  # Flag per il logging
        self.log_file = "clipboardGPT_log.txt"  # Nome del file di log
        self.last_response = ""  # Variabile per tracciare l'ultima risposta

        # Configura l'interfaccia utente e avvia il thread di monitoraggio della clipboard
        self.setup_ui()
        self.clipboard_monitoring_thread = threading.Thread(target=self.monitor_clipboard)
        self.clipboard_monitoring_thread.daemon = True
        self.clipboard_monitoring_thread.start()

    def setup_ui(self):
        # Configurazione dell'interfaccia utente
        self.root.title("ClipboardGPT")
        self.root.geometry("300x250")
        self.root.attributes('-topmost', True)

        # Pulsanti e dropdown per l'interazione dell'utente
        self.toggle_button = Button(self.root, text="Activate", command=self.toggle_active)
        self.toggle_button.pack(pady=10)

        self.status_indicator = Canvas(self.root, width=20, height=20, bg='white')
        self.status_indicator.pack(pady=5)
        self.update_status_indicator(False)

        self.model_var = StringVar(value="GPT-3.5 Turbo")
        self.model_menu = OptionMenu(self.root, self.model_var, "GPT-3.5 Turbo", "GPT-4 Turbo", command=self.set_model)
        self.model_menu.pack(pady=10)

        self.api_key_button = Button(self.root, text="Set API Key", command=self.set_api_key)
        self.api_key_button.pack(pady=10)

        self.prefix_button = Button(self.root, text="Set Command Prefix", command=self.set_prefix)
        self.prefix_button.pack(pady=10)

        # Nasconde inizialmente il pulsante di logging
        self.logging_button = Button(self.root, text="Enable Logging", command=self.toggle_logging)
        self.root.bind("<Control-l>", self.toggle_logging_visibility)

    def toggle_active(self):
        # Attiva/disattiva lo stato dell'app
        self.active = not self.active
        self.toggle_button.config(text="Deactivate" if self.active else "Activate")
        self.update_status_indicator(self.active)
        self.log(f"App {'activated' if self.active else 'deactivated'}")

    def update_status_indicator(self, is_active):
        # Aggiorna l'indicatore di stato (pallino verde/rosso)
        color = "green" if is_active else "red"
        self.status_indicator.create_oval(5, 5, 15, 15, fill=color, outline="")

    def toggle_logging_visibility(self, event=None):
        # Mostra/nasconde il pulsante di logging
        if self.logging_button.winfo_ismapped():
            self.logging_button.pack_forget()
        else:
            self.logging_button.pack(pady=10)

    def set_model(self, model):
        # Imposta il modello per l'API OpenAI
        self.model = "gpt-3.5-turbo-1106" if model == "GPT-3.5 Turbo" else "gpt-4-1106-preview"
        self.log(f"Model set to: {self.model}")

    def set_api_key(self):
        # Imposta la chiave API OpenAI
        self.api_key = simpledialog.askstring("API Key", "Enter your OpenAI API key:", parent=self.root)
        if self.api_key:
            self.log("API key set.")

    def set_prefix(self):
        # Imposta il prefisso per i comandi
        self.prefix = simpledialog.askstring("Command Prefix", "Enter command prefix:", parent=self.root)
        self.log(f"Prefix set to: {self.prefix}")

    def toggle_logging(self):
        # Attiva/disattiva il logging
        self.logging_enabled = not self.logging_enabled
        self.log("Logging " + ("enabled" if self.logging_enabled else "disabled"))

    def monitor_clipboard(self):
        # Monitora continuamente la clipboard per nuovo testo
        previous_text = ""
        while True:
            if self.active:
                text = pyperclip.paste()
                if text != previous_text and text != self.last_response:
                    self.root.config(cursor="wait")
                    previous_text = text
                    self.process_clipboard_text(text)
                    self.root.config(cursor="")
            time.sleep(1)

    def process_clipboard_text(self, text):
        # Elabora il testo dalla clipboard usando l'API OpenAI
        prompt = f"{self.prefix} {text}"
        response = self.query_openai(prompt)
        if response:
            pyperclip.copy(response)
            self.log(f"Processed text. Prompt: {prompt}")
            self.last_response = response

    def query_openai(self, prompt):
        # Invia una richiesta all'API OpenAI e ritorna la risposta
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        if response.ok:
            self.log("API request successful.")
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        else:
            self.log(f"API request failed. Status code: {response.status_code}")
            return ""

    def log(self, message):
        # Registra i messaggi in un file di log
        if self.logging_enabled:
            with open(self.log_file, "a") as log_file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"{timestamp}: {message}\n")

if __name__ == "__main__":
    root = Tk()
    app = ClipboardGPTApp(root)
    root.mainloop()