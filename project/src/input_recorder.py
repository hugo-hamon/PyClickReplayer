from typing import Any, List, Tuple, Union, Set
from pynput import keyboard, mouse
from pathlib import Path
import contextlib
import logging
import json
import time


class InputRecorder:

    def __init__(self, script_path: str) -> None:
        self.script_path = script_path
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press, on_release=self.on_key_release)
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.inputs: List[Tuple[str, Any, float]] = []
        self.keys_pressed: Set = set()
        self.start_time = time.time()
        self.recording = True

    def on_key_press(self, key: Union[keyboard.Key, keyboard.KeyCode, None]) -> None:
        """Record the key press event."""
        self.keys_pressed.add(key)
        if isinstance(key, keyboard.Key):
            self.inputs.append(
                ('key_press', key.name, time.time() - self.start_time))
        elif isinstance(key, keyboard.KeyCode):
            self.inputs.append(
                ('key_press', key.char, time.time() - self.start_time))
        self.start_time = time.time()

        if keyboard.Key.f1 in self.keys_pressed:
            self.stop_recording()

    def on_key_release(self, key: Union[keyboard.Key, keyboard.KeyCode, None]) -> None:
        """Record the key release event."""
        with contextlib.suppress(KeyError):
            self.keys_pressed.remove(key)

    def on_mouse_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        """Record the mouse click event."""
        if not pressed:
            return
        current_time = time.time() - self.start_time
        self.inputs.append(
            ('mouse_click', (x, y, button.name, pressed, 1), current_time)
        )
        self.start_time = time.time()

    def record(self) -> None:
        """Start recording the inputs of keyboard and mouse."""
        logging.info(
            "Debut de l'enregistrement. Appuyez sur F1 pour arrêter.")
        with self.keyboard_listener, self.mouse_listener:
            self.keyboard_listener.join()
            self.mouse_listener.join()
        logging.info("Fin de l'enregistrement.")

    def save(self) -> None:
        """Save the inputs in a json file."""
        file_path = f"inputs/{self.script_path}"
        with open(file_path, 'w') as file:
            json.dump(self.inputs[:-1], file, indent=4)
        logging.info(
            f"Les entrées ont été sauvegardées dans le fichier {file_path}.")

    def stop_recording(self):
        """Stop the recording."""
        self.recording = False
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        self.save()
