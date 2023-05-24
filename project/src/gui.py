from .loggingHandler import LoggingHandler
from .input_recorder import InputRecorder
from .input_replayer import InputReplayer
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import N, S, E, W
from tkinter import ttk
import tkinter as tk
import threading
import logging
import json


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

        # Log en temps réel
        self.log_label = ttk.Label(self, text="Logs:")
        self.log_label.pack()
        self.log_text = scrolledtext.ScrolledText(self, width=50, height=10)
        self.log_text.pack()

        # Configurer le gestionnaire de log pour rediriger vers la zone de texte
        log_handler = LoggingHandler(self.log_text)
        log_formatter = logging.Formatter(
            "%(asctime)s\n%(message)s", "%H:%M:%S")
        log_handler.setFormatter(log_formatter)

        # Ajouter le gestionnaire au logger
        logging.getLogger().addHandler(log_handler)
        logging.getLogger().setLevel(logging.INFO)

        self.mode.trace("w", self.update_ui)
        self.update_ui()

    def start(self) -> None:
        """Lance le record ou le replay avec les paramètres choisis par l'utilisateur."""
        mode = self.mode.get()
        file_name = self.file_entry.get()
        loop = self.loop.get()
        no_delay = self.no_delay.get()
        logging.info(
            f"Mode: {mode}, File: {file_name}, Loop: {loop}, No-Delay: {no_delay}"
        )
        if mode == "record":
            input_recorder = InputRecorder(file_name)
            threading.Thread(target=input_recorder.record,
                             daemon=True).start()
        elif mode == "replay":
            file_names = file_name.split(", ")
            print(file_names)
            if len(file_names) > 1:
                self.combined_input()
            input_replayer = InputReplayer(file_names[0] if len(file_names) == 1
                                           else "inputs/combined_input.json")
            threading.Thread(target=input_replayer.replay, args=(loop, no_delay),
                             daemon=True).start()
        self.update_ui()

    def load_file(self) -> None:
        """Charge un fichier json."""
        if file_paths := filedialog.askopenfilenames(
            filetypes=(("json files", "*.json"), ("all files", "*.*"))
        ):
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, ", ".join(file_paths))

    def update_ui(self, *args) -> None:
        """Update the user interface based on the selected mode.""" 
        if self.mode.get() == "record":
            self.loop_checkbox.pack_forget()
            self.no_delay_checkbox.pack_forget()
            self.load_button.pack_forget()
            self.file_entry.delete(0, 'end')
        else:
            self.start_button.pack_forget()
            self.log_text.pack_forget()
            self.log_label.pack_forget()
            self.load_button.pack()
            self.loop_checkbox.pack()
            self.no_delay_checkbox.pack()
            self.start_button.pack()
            self.log_label.pack()
            self.log_text.pack()

    def combined_input(self) -> None:
        """Combine the input from the mouse and keyboard."""
        combined_inputs = []
        for file in self.file_entry.get().split(", "):
            with open(file, "r") as f:
                data = json.load(f)
            combined_inputs.extend(data)

        file_name = "inputs/combined_input.json"
        with open(file_name, "w") as f:
            json.dump(combined_inputs, f)
