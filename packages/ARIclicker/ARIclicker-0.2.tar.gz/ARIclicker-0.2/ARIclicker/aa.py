
import pyautogui
import keyboard
import time
import threading
def func(key_start,key_stop):
       while True:
            keyboard.wait(key_start)
            time.sleep(0.1)
            while True:
                pyautogui.click()
                if keyboard.is_pressed(key_stop):
                    time.sleep(0.1)
                    break
t1=threading.Thread(target=func,args=('a','b'))
t1.start()
