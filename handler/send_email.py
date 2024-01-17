import os
from email.message import EmailMessage
import ssl
import smtplib
from dotenv import load_dotenv
load_dotenv()

def email_verification(emailreceiver, verificationcode):

    email_sender = "cryptofortmail@gmail.com"
    email_password = os.environ.get('EMAIL_PASSWORD')


    subject = "Verification code"
    body  = f""" Your Verification code for Email:'{emailreceiver}' is {verificationcode}  """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = emailreceiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, emailreceiver, em.as_string())


