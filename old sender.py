from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import csv
import time
import random
import os
from dotenv import load_dotenv

def send_email(sender_email, sender_password, smtp_server, smtp_port, recipient_email, paper_title):
    subject = "Invitation to CSAC Conference"
    body = f"""\
    <html>
      <body>
        <p>Hello,<br><br>
        I hope you are doing well. We're intrigued by your research: <strong>{paper_title}</strong>.<br><br>
        We would like to invite you to present at the <strong>Computer Science Advancements Conference (CSAC)</strong>, which will be a virtual conference on<strong> October 19th, 2024 at 20:00 UTC (3:00 PM CST)</strong>. This conference consists of presentations from other cutting edge researchers in various Computer Science fields, covering a wide range of topics.<br><br>
        Registering and presenting is free of charge for researchers that are receiving this invitation. This is a <strong>virtual conference</strong>, so presenters will submit a 10-15 minute recording of their keynote research presentation. Attendance in the live conference is highly encouraged in order to answer audience questions, but not mandatory.<br><br>

        If you are interested, please use the following link to register your paper: <a href=''>Registration Link</a>.<br>

        
        This code is <strong>UNIQUE</strong> to your research paper. Enter it in the appropriate field when registering. <strong>Do NOT share this code with anyone.</strong> <br><br>
        <mark>Unique Registration Code: <strong>{random.randint(10000,99999)}</strong> </mark> </br>

        
        <br><br>
        <strong>About Pubnect:</strong><br><br>
        Pubnect is a platform designed to bridge the gap between researchers/publishers and the broader academic community. By focusing on virtual conferences, we offer an accessible way for researchers to present their work to a global audience. Learn more about Pubnect and CSAC at pubnect.com<br><br>
        Sincerely,<br>
        <strong>Pubnect Team</strong>
        </p>
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    server.sendmail(sender_email, recipient_email, msg.as_string())
    print(f"Email sent successfully to {recipient_email}!")

    server.quit()

def send_emails_from_csv(sender_email, sender_password, smtp_server, smtp_port, csv_filename):
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipient_email = row['email']
            paper_title = row['title']
            retries = 3  
            while retries > 0:
                try:
                    send_email(sender_email, sender_password, smtp_server, smtp_port, recipient_email, paper_title)
                    break  
                except Exception as e:
                    print(f"Error sending email to {recipient_email}: {e}")
                    retries -= 1
                    if retries == 0:
                        print("Maximum retries reached. Moving to the next email.")
                    else:
                        print(f"Retrying... {retries}")
                        time.sleep(61)


sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = int(os.getenv('SMTP_PORT'))
csv_filename = os.getenv('CSV_FILENAME')

send_emails_from_csv(sender_email, sender_password, smtp_server, smtp_port, csv_filename)