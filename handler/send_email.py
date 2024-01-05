import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, message, sender_email, receiver_email, password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")


sender_email = 'your_email@yahoo.com'
receiver_email = 'recipient_email@example.com'
password = 'your_password'
subject = 'Test Email'
message = 'This is a test email sent from Python!'

send_email(subject, message, sender_email, receiver_email, password)
