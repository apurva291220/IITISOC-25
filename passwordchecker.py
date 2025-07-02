import re #to detect pattern, regular expression
import string

#COMMON_PASSWORDS = {"password","QWERTY", "123456", "qwerty", "abcd", "welcome", "abc123", "1111111"}  # Example set
def load_common_passwords(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        return set(line.strip().lower() for line in f if line.strip())
COMMON_PASSWORDS = load_common_passwords('common-passwords.txt')


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

if __name__ == "__main__":
    password = input("Enter your password: ")
    print(f"-> Password Length: {len(password)}") 
    strength, recommendations = check_password_strength(password)
    print(f"-> Password Strength: {strength}")
    if recommendations:
        print("-> Recommendations to improve your password:")
        for rec in recommendations:
            print(f"   - {rec}")
    else:
        print("Your password is strong. Good job!")
