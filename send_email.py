import smtplib
from email.message import EmailMessage
import getpass

def send_email(subject='Test Email from Python', 
               message='Hello! This is a test email sent from Python.'):
    # Set up your email and app PW
    gmail_user = 'jiminkangtest@gmail.com'
    gmail_pw = "fgma ungh sqnk mlov" # App PW for 'Python Script'

    # Create the email content
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = gmail_user
    msg.set_content(message)

    # Connect to Gmail SMTP server and send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(gmail_user, gmail_pw)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email()