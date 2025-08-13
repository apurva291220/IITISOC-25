import tkinter as tk
import os, subprocess, platform
from tkinter import messagebox
import webbrowser
import sys

from passswordchecker import password_guiintegrated
from mailicious_mail_identifier import malicious_guiintegrated
from File_Integreity_Checker import integritychecker_guiintegrated

# Appearance
BG_COLOR = "#f3f3f6"     
BTN_COLOR = "#050505"     
BTN_TEXT_COLOR = "white"
FONT_HEADER = ("Cambria", 20, "bold")
FONT_BUTTON = ("Cambria", 12, "bold")

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def open_user_manual(): #usermanual
    manual_path = os.path.join(os.path.dirname(__file__), "User_Manual.docx")
    if not os.path.exists(manual_path):
        messagebox.showerror("Error", f"Manual not found: {manual_path}")
        return
    try:
        system = platform.system()
        if system == "Windows":
            os.startfile(manual_path)
        elif system == "Darwin":  # macOS
            subprocess.call(["open", manual_path])
        else:  # Linux or others
            subprocess.call(["xdg-open", manual_path])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open the manual:\n{e}")

def load_keylogger_demo(frame, back_callback):
    """Load the keylogger/phishing demo interface"""
    clear_frame(frame)
    
    # Back button
    tk.Button(frame, text="← Back", command=back_callback).pack(anchor="nw", padx=10, pady=10)
    
    # Main content
    content_frame = tk.Frame(frame, bg=BG_COLOR)
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    tk.Label(content_frame, text="Keylogger & Phishing Demo", 
             font=FONT_HEADER, bg=BG_COLOR).pack(pady=20)
    
    def start_demo():
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Open phishing page - assuming ph.html is in a subfolder called 'phishing_demo'
            phishing_dir = os.path.join(script_dir, "phishing demo")
            if not os.path.exists(phishing_dir):
                os.makedirs(phishing_dir)
                
            phishing_file = os.path.join(phishing_dir, "ph.html")
            if not os.path.exists(phishing_file):
                # Create a simple phishing demo file if it doesn't exist
                with open(phishing_file, "w") as f:
                    f.write("""<html><body><h1>Phishing Demo Page</h1></body></html>""")
            
            webbrowser.open(f"file://{phishing_file}")
            
            # Start keylogger - assuming keylogger.py is in the same directory
            keylogger_path = os.path.join(script_dir, "keylogger.py")
            subprocess.Popen(["python", keylogger_path], shell=True)
            
            messagebox.showinfo("Demo Started", "Phishing page and keylogger started successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start demo:\n{e}")

    def open_logged_file():
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            log_file = os.path.join(script_dir, "keylogger.txt")
            if os.path.exists(log_file):
                if sys.platform == "win32":
                    os.startfile(log_file)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, log_file])
            else:
                messagebox.showinfo("Info", "No log file found yet")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open log file:\n{e}")

    button_frame = tk.Frame(content_frame, bg=BG_COLOR)
    button_frame.place(relx=0.5, rely=0.5, anchor="center")
    #start button
    tk.Button(content_frame, text="Start Demo", command=start_demo,
              font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
              width=20, height=2).pack(pady=20)
    #warning
    tk.Label(content_frame, text="Warning: This will open a phishing demo page\nand start a keylogger simulation", 
             font=("Cambria", 10), bg=BG_COLOR).pack()
    #stop 
    tk.Label(content_frame, text="Press esc to stop keylogger", 
             font=("Cambria", 10), bg=BG_COLOR, color=Red).pack()
    #view log file
    tk.Button(button_frame, text="View Log File", width=25, height=2,
              font=FONT_BUTTON, bg="#090909", fg="white",
              command=open_logged_file).grid(row=4, column=0, pady=10)

def main():
    root = tk.Tk()
    root.title("Cybersecurity Suite")
    root.geometry("900x600")

    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)

    def show_main_menu():
        clear_frame(content_frame)

        tk.Label(content_frame, text="Select Tool", font=FONT_HEADER, bg=BG_COLOR, 
                 fg="#0B0B0C").place(relx=0.5, rely=0.15, anchor="center")

        button_frame = tk.Frame(content_frame, bg=BG_COLOR)
        button_frame.place(relx=0.5, rely=0.5, anchor="center")
       
        # Password Checker Button
        tk.Button(button_frame, text="Password Checker", width=25, height=2,
                  font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
                  command=lambda: password_guiintegrated.load_ui(content_frame, show_main_menu)).grid(row=0, column=0, pady=10)

        # Malicious Email Scanner Button
        tk.Button(button_frame, text="Malicious Email Scanner", width=25, height=2,
                  font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
                  command=lambda: malicious_guiintegrated.load_ui(content_frame, show_main_menu)).grid(row=1, column=0, pady=10)
        
        # Keylogger/Phishing Demo Button
        tk.Button(button_frame, text="Keylogger and Phishing Demo", width=25, height=2,
                  font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
                  command=lambda: load_keylogger_demo(content_frame, show_main_menu)).grid(row=3, column=0, pady=10)
        
        # File Integrity Checker Button
        tk.Button(button_frame, text="File Integrity Checker", width=25, height=2,
                  font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
                  command=lambda: integritychecker_guiintegrated.load_ui(content_frame, show_main_menu)).grid(row=2, column=0, pady=10)

        # User Manual Button
        tk.Button(button_frame, text="User Manual", width=25, height=2,
                  font=FONT_BUTTON, bg="#090909", fg="white",
                  command=open_user_manual).grid(row=4, column=0, pady=10)

    show_main_menu()
    root.mainloop()

if __name__ == "__main__":
    main()
    

    

