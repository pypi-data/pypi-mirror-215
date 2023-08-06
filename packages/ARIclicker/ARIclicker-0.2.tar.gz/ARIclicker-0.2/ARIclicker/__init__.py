import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import pynput
import random
import pyautogui
import keyboard

class ClickMouse(threading.Thread):
    def __init__(self, delay_min, delay_max, button):
        super(ClickMouse, self).__init__()
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        mouse=Controller()
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(random.uniform(self.delay_min, self.delay_max))


def autoclick(start_stop_key_character, end_key_character, delay_min, delay_max, button):
    if button == "left":
        button = Button.left
    if button == "right":
        button = Button.right
    start_stop_key = KeyCode(char=start_stop_key_character)
    stop_key = KeyCode(char=end_key_character)
    mouse = pynput.mouse.Controller()
    click_thread = ClickMouse(delay_min, delay_max, button)
    click_thread.start()

    def on_press(key):
        if key == start_stop_key:
            if click_thread.running:
                click_thread.stop_clicking()
            else:
                click_thread.start_clicking()
        elif key == stop_key:
            click_thread.exit()
            listener.stop()

    with Listener(on_press=on_press) as listener:
        listener.join()
        start_listening_click = True



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
    press_thread = PressKey(button)
    press_thread.start()

    def on_press(key):
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

def quickclick(key_start,key_stop):
  
    def func(key_start,key_stop):
       while True:
            keyboard.wait(key_start)
            time.sleep(0.1)
            while True:
                pyautogui.click()
                if keyboard.is_pressed(key_stop):
                    time.sleep(0.1)
                    break
    t1=threading.Thread(target=func,args=(key_start,key_stop))
    t1.start()

