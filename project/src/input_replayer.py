from typing import Any, List, Tuple
from pynput import keyboard, mouse
import pydirectinput
import threading
import logging
import time
import json


CLICK_FRACTION = 100


class InputReplayer:
    def __init__(self, script_path: str) -> None:
        self.script_path = script_path

        self.inputs = self.load_inputs()
        self.stop_inputs = []
        self.stop_replay = False

        self.controller_keyboard = keyboard.Controller()
        self.controller_mouse = mouse.Controller()

    def load_inputs(self) -> List[Tuple[str, Any, float]]:
        """Charge les entrées à partir du fichier."""
        with open(self.script_path, 'r') as file:
            data = json.load(file)
        return data

    def replay(self, loop: bool = False, no_delay: bool = False) -> None:
        """Rejoue les entrées lues à partir du fichier."""
        self.stop_replay = False
        replay_thread = threading.Thread(
            target=self.replay_thread_func, args=(loop, no_delay)
        )
        replay_thread.start()
        listener = keyboard.Listener(on_release=self.on_key_release)
        listener.start()
        while not self.stop_replay:
            time.sleep(1)

        listener.stop()
        replay_thread.join()

    def replay_thread_func(self, loop: bool, no_delay: bool) -> None:
        logging.info("Debut de la relecture.")
        while not self.stop_replay:
            for event, params, delay in self.inputs:
                if self.stop_replay:
                    break
                if delay > 0 and not no_delay:
                    time.sleep(delay)
                self.execute(event, params)
            if not loop:
                self.stop_replay = True
        logging.info("Fin de la relecture.")

    def execute(self, event: str, params: Any) -> None:
        """Rejoue les entrées lues à partir du fichier."""
        if event == 'key_press':
            try:
                key = keyboard.Key[params]
            except KeyError:
                key = keyboard.KeyCode.from_char(params)
            self.controller_keyboard.press(key)
            self.controller_keyboard.release(key)
        elif event == 'mouse_click':
            x, y, _, _, click_nb = params
            self.controller_mouse.position = (x, y)
            if click_nb < CLICK_FRACTION:
                pydirectinput.click(x=x, y=y, clicks=click_nb, interval=1e-4)
            else:
                for _ in range(click_nb // CLICK_FRACTION):
                    if self.stop_replay:
                        return
                    pydirectinput.click(
                        x=x, y=y, clicks=CLICK_FRACTION, interval=1e-4
                    )
                if self.stop_replay:
                    return
                pydirectinput.click(
                    x=x, y=y, clicks=click_nb % CLICK_FRACTION, interval=1e-4
                )

    def on_key_release(self, key) -> None:
        self.stop_inputs.append(key)
        if keyboard.Key.ctrl_l in self.stop_inputs and keyboard.Key.alt_l in self.stop_inputs:
            self.stop_replay = True
        if len(self.stop_inputs) > 10:
            self.stop_inputs.pop(0)
