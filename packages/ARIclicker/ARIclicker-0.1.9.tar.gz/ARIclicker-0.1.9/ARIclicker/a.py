import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import pynput
import random


def autopress(start_stop_key_character, end_key_character, button):
    class PressKey(threading.Thread):
        def __init__(self, button):
            super(PressKey, self).__init__()
            self.button = button
            self.running = False
            self.program_running = True

        def start_pressing(self):
            self.running = True

        def stop_pressing(self):
            self.running = False

        def exit(self):
            self.stop_pressing()
            self.program_running = False

        def run(self):
            key = pynput.keyboard.Controller()
            while self.program_running:
                while self.running:
                    key.press(button)

    start_stop_key = KeyCode(char=start_stop_key_character)
    stop_key = KeyCode(char=end_key_character)
    print(start_stop_key)
    press_thread = PressKey(button)
    press_thread.start()

    def on_press(key):
        print(key)
        if key == start_stop_key:
            if press_thread.running:
                press_thread.stop_pressing()
            else:
                press_thread.start_pressing()
        elif key == stop_key:
            press_thread.exit()
            listener.stop()
          
    with Listener(on_press=on_press) as listener:
        listener.join()

autopress("q","w","e")
