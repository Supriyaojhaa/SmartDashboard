import re

def validate_user(name, email, phone, password):

    name_pattern = r"^[A-Za-z ]+$"
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    phone_pattern = r"^[0-9]{10}$"
    password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$"

    if not re.match(name_pattern, name):
        return "Invalid Name"

    if not re.match(email_pattern, email):
        return "Invalid Email"

    if not re.match(phone_pattern, phone):
        return "Invalid Phone Number"

    if not re.match(password_pattern, password):
        return "Password must contain letters and numbers"

    return "Valid"