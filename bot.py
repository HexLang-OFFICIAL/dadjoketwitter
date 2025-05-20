import smtplib
import requests
import os
import json
from email.message import EmailMessage
from email.utils import formataddr

# Load recipients from a JSON file or env variable (for demo, JSON file)
def load_recipients(filename="recipients.json"):
    with open(filename, "r") as f:
        return json.load(f)

# Get multiple jokes from API (or fallback to local jokes)
def get_dad_jokes(count=5):
    jokes = []
    headers = {"Accept": "application/json"}
    for _ in range(count):
        try:
            res = requests.get("https://icanhazdadjoke.com/", headers=headers, timeout=5)
            if res.status_code == 200:
                jokes.append(res.json()["joke"])
            else:
                jokes.append("No dad joke today, blame the API.")
        except Exception:
            jokes.append("Dad joke API is taking a nap, here's a backup: Why don’t skeletons fight each other? They don’t have the guts.")
    return jokes

# Format jokes as an HTML list for the newsletter
def format_jokes_html(jokes):
    jokes_html = "<ul>"
    for joke in jokes:
        jokes_html += f"<li>{joke}</li>"
    jokes_html += "</ul>"
    return jokes_html

# Build personalized HTML email content
def build_email_content(name, jokes):
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #fdf6e3; color: #586e75;">
        <h2>Hey {name}, here’s your weekly dose of dad jokes! 🤪</h2>
        {format_jokes_html(jokes)}
        <p style="font-style: italic; color: #657b83;">
          Brought to you by the Dad Joke Bot. Because laughter is the best medicine (except for real medicine).
        </p>
      </body>
    </html>
    """
    return html_content

# Send HTML email
def send_email(subject, html_content, to_email, from_email, from_name, password):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((from_name, from_email))
    msg["To"] = to_email
    msg.set_content("Your email client does not support HTML. Here's your dad joke newsletter in plain text.")
    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)
        print(f"Email sent to {to_email}")

if __name__ == "__main__":
    # Load email credentials & sender info from secrets/env
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    FROM_NAME = os.getenv("FROM_NAME", "Dad Joke Bot")

    # Load recipients from JSON file in repo
    recipients = load_recipients()

    # Get 5 jokes for newsletter
    jokes = get_dad_jokes(5)

    # Send personalized emails
    for r in recipients:
        name = r.get("name", "Friend")
        email = r["email"]
        html_email = build_email_content(name, jokes)
        send_email("Your Weekly Dad Joke Newsletter 🤪", html_email, email, EMAIL_ADDRESS, FROM_NAME, EMAIL_PASSWORD)
