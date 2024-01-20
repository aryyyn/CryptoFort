import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
from dotenv import load_dotenv
load_dotenv()

def email_verification(emailreceiver, verificationcode):

    email_sender = "cryptofortmail@gmail.com"
    email_password = os.environ.get('EMAIL_PASSWORD')

    subject = "Verification Code"
    
    body = f"""<html>
<head>
     <style>
        body {{
            font-family: 'Courier New', monospace;
            background-color: #000;
            color: #00ff00;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #000;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        header {{
            padding: 20px;
            text-align: center;
            background-color: #000;
            color: #00ff00;
            border-bottom: 2px solid #00ff00;
        }}
        header img {{
            max-width: 100px;
            height: auto;
        }}
        .content {{
            padding: 20px;
        }}
        p {{
            color: #00ff00;
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 15px;
        }}
        strong {{
            color: #00ff00;
            font-weight: bold;
        }}
        footer {{
            text-align: center;
            padding: 10px;
            background-color: #000;
            color: #00ff00;
            border-top: 2px solid #00ff00;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <img src="https://cdn.discordapp.com/attachments/802863234343895064/1198190763339694193/image.png" alt="Logo">
        </header>

        <div class="content">
            <p>Hi,</p>

            <p>Your code for email <strong>{emailreceiver}</strong> is <strong>{verificationcode}.</strong></p>
        </div>
        <footer>
            CryptoFort
        </footer>
    </div>
</body>
</html>"""

    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = emailreceiver
    em['Subject'] = subject

    # Attach the HTML content
    em.attach(MIMEText(body, 'html'))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, emailreceiver, em.as_string())

# Call the function with the appropriate parameters

