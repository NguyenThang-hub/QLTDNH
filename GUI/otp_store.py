import json
import os

OTP_FILE = "otp_data.json"

def save_otp(username, otp):
    with open(OTP_FILE, "w") as f:
        json.dump({"username": username, "otp": otp}, f)

def load_otp():
    if os.path.exists(OTP_FILE):
        with open(OTP_FILE, "r") as f:
            return json.load(f)
    return {}

def delete_otp():
    if os.path.exists(OTP_FILE):
        os.remove(OTP_FILE)
