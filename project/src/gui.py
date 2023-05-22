from .loggingHandler import LoggingHandler
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import logging


class Application(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("PyClickReplayer")
        self.geometry("500x500")

        # Choix entre Record et Replay
        self.mode = tk.StringVar()
        self.mode.set("record")
        self.mode_options = ttk.OptionMenu(
            self, self.mode, "record", "record", "replay"
        )
        self.mode_options.pack()

        # Entrée pour le nom de fichier
        self.file_label = ttk.Label(self, text="Nom du fichier:")
        self.file_label.pack()
        self.file_entry = ttk.Entry(self)
        self.file_entry.pack()

        # Bouton pour charger un fichier
        self.load_button = ttk.Button(
            self, text="Load", command=self.load_file
        )
        self.load_button.pack()

        # Bouton pour sauvegarder un fichier
        self.save_button = ttk.Button(
            self, text="Save", command=self.save_file
        )
        self.save_button.pack()

        # Checkbox pour l'option Loop
        self.loop = tk.BooleanVar()
        self.loop_checkbox = ttk.Checkbutton(
            self, text="Loop", variable=self.loop
        )
        self.loop_checkbox.pack()

        # Checkbox pour l'option No-Delay
        self.no_delay = tk.BooleanVar()
        self.no_delay_checkbox = ttk.Checkbutton(
            self, text="No-Delay", variable=self.no_delay
        )
        self.no_delay_checkbox.pack()

        # Bouton Start
        self.start_button = ttk.Button(self, text="Start", command=self.start)
        self.start_button.pack()

        # Bouton Stop
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop)
        self.stop_button.pack()

        # Log en temps réel
        self.log_label = ttk.Label(self, text="Logs:")
        self.log_label.pack()
        self.log_text = scrolledtext.ScrolledText(self, width=40, height=10)
        self.log_text.pack()

        # Configurer le gestionnaire de log pour rediriger vers la zone de texte
        log_handler = LoggingHandler(self.log_text)
        log_formatter = logging.Formatter("%(asctime)s\n%(message)s", "%H:%M:%S")
        log_handler.setFormatter(log_formatter)

        # Ajouter le gestionnaire au logger
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.INFO)

    def start(self) -> None:
        """Lance le record ou le replay avec les paramètres choisis par l'utilisateur."""
        mode = self.mode.get()
        file_name = self.file_entry.get()
        loop = self.loop.get()
        no_delay = self.no_delay.get()
        logging.info(
            f"Mode: {mode}, File: {file_name}, Loop: {loop}, No-Delay: {no_delay}"
        )
        # TODO: Lancer le record ou le replay avec les paramètres choisis par l'utilisateur.

    def stop(self) -> None:
        """Arrête le record ou le replay."""
        logging.info("Stop")
        # TODO: Arrêter le record ou le replay.

    def load_file(self) -> None:
        """Charge un fichier json."""
        if file_path := filedialog.askopenfilename(
            filetypes=(("json files", "*.json"), ("all files", "*.*"))
        ):
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, file_path)

    def save_file(self) -> None:
        """Sauvegarde un fichier json."""
        if file_path := filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=(("json files", "*.json"), ("all files", "*.*")),
        ):
            self.file_entry.delete(0, 'end')
