import smtplib
import requests
import os
from email.message import EmailMessage

def get_dad_joke():
    headers = {"Accept": "application/json"}
    res = requests.get("https://icanhazdadjoke.com/", headers=headers)
    if res.status_code == 200:
        return res.json()["joke"]
    else:
        return "No dad joke today. Blame the API."

def send_email(subject, body, to_email):
    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)
        print("Email sent!")

if __name__ == "__main__":
    joke = get_dad_joke()
    send_email("Your Daily Dad Joke 🤪", joke, os.getenv("TO_EMAIL"))
