from pynput.keyboard import Key, Controller, Listener
from pynput import keyboard
from time import sleep

keyboard = Controller()
while True:
    sleep(60)
    keyboard.press(Key.shift)
    keyboard.release(Key.shift)
