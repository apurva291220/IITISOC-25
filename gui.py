import tkinter as tk
import os, subprocess, platform
from tkinter import messagebox
import webbrowser
from tkPDFViewer import tkPDFViewer as pdf

import password_guiintegrated
import malicious_guiintegrated
import integritychecker_guiintegrated

# Appearance
BG_COLOR = "#f3f3f6"     
BTN_COLOR = "#050505"     
BTN_TEXT_COLOR = "white"
FONT_HEADER = ("Cambria", 20, "bold")
FONT_BUTTON = ("Cambria", 12, "bold")

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def open_user_manual():
    manual_path = os.path.join(os.path.dirname(__file__), "User_Manual.pdf")
    if not os.path.exists(manual_path):
        messagebox.showerror("Error", f"Manual not found: {manual_path}")
        return
    viewer_win = tk.Toplevel()
    viewer_win.title("User Manual")
    viewer_win.geometry("700x800")

    v1 = pdf.ShowPdf()
    pdf_display = v1.pdf_view(viewer_win, pdf_location=manual_path, width=100, height=100)
    pdf_display.pack(fill="both", expand=True)

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
            # Open phishing page
            url = "file:///C:/Users/apurv/OneDrive/Desktop/study%20materials/cybersecurity/kelogger/src/phishing%20demo/ph.html"
            webbrowser.open(url)
            
            # Start keylogger
            keylogger_path = r"C:\Users\apurv\OneDrive\Desktop\study materials\cybersecurity\kelogger\src\keylogger.py"
            subprocess.Popen(["python", keylogger_path], shell=True)
            
            messagebox.showinfo("Demo Started", "Phishing page and keylogger started successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start demo:\n{e}")

    tk.Button(content_frame, text="Start Demo", command=start_demo,
              font=FONT_BUTTON, bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
              width=20, height=2).pack(pady=20)
    
    tk.Label(content_frame, text="Warning: This will open a phishing demo page\nand start a keylogger simulation", 
             font=("Cambria", 10), bg=BG_COLOR).pack()

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
    

    
