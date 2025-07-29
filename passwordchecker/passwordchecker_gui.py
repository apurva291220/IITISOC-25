import re #to detect pattern, regular expression
import string
import tkinter as tk
from tkinter import messagebox

#COMMON_PASSWORDS = {"password","QWERTY", "123456", "qwerty", "abcd", "welcome", "abc123", "1111111"}  # Example set
def load_common_passwords(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        return set(line.strip().lower() for line in f if line.strip())
COMMON_PASSWORDS = load_common_passwords('common_password.txt')


def check_password_strength(password):
    recommendations = [] #suggestions
    score = 0 

    # Check length
    length = len(password)
    if length < 6:
        recommendations.append("Password too short! Must be at least 6 characters.")
        score += 1
    elif length >= 6:
        score += 2
    else:
        score += 1

    # Common patterns
    if password.lower() in COMMON_PASSWORDS:
        recommendations.append("Avoid common passwords.")
        score = 0  # if password is common,it is considered weak.
    if re.search(r'(.)\1\1', password):
        recommendations.append("Avoid repeated characters or simple patterns.")

    # Character variety
    has_upper = any(c.isupper() for c in password) #uppercase
    has_lower = any(c.islower() for c in password) #lowercase
    has_digit = any(c.isdigit() for c in password) #digit
    has_symbol = any(c in string.punctuation for c in password) #symbol
    
    #check if passowrd contains atleast of all, if any character is missing recommendation is added,if present score is increased
    if not has_upper:
        recommendations.append("Add at least one uppercase letter.")
    else:
        score += 1
    if not has_lower:
        recommendations.append("Add at least one lowercase letter.")
    else:
        score += 1
    if not has_digit:
        recommendations.append("Add at least one digit.")
    else:
        score += 1
    if not has_symbol:
        recommendations.append("Add at least one special symbol (e.g., !, @, #, $).")
    else:
        score += 1

    # Classification based on score
    if score <= 3:
        strength = "Weak"
    elif 4 <= score <= 5:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, recommendations

def load_ui(frame, back_callback): #load GUI into frame
    for widget in frame.winfo_children():
        widget.destroy()

    tk.Button(frame, text="← Back", command=back_callback).pack(anchor="nw", padx=10, pady=10)
     
    tk.Label(frame, text="Enter your password:", font=("Cambria", 16, "bold")).pack(pady=10)
    # Password entry
    entry_var = tk.StringVar()
    entry = tk.Entry(frame, textvariable=entry_var, show="*", width=60)
    entry.pack(pady=5)

# Toggle show/hide
    def toggle_password():
      if show_password_var.get():
        entry.config(show="")  # Show password
      else:
        entry.config(show="*")  # Hide password

    show_password_var = tk.BooleanVar()
    tk.Checkbutton(frame, text="Show Password", variable=show_password_var, command=toggle_password).pack(pady=5)


    def check():
      password = entry.get()
      strength, recommendations = check_password_strength(password)
      result = f"Password Strength: {strength}\n\n"
      result += "\n".join(f"- {r}" for r in recommendations) if recommendations else "Your password is strong!"
      messagebox.showinfo("Result", result)

    tk.Button(frame, text="Check Strength",  font=("Cambria", 14, "bold"), command=check).pack(pady=15)    
