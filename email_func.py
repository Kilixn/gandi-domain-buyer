import smtplib, ssl
from parameters import email_address, email_password, email_server, reciever_email

port = 587  # For starttls

def send_email(subject, message):
    context = ssl.create_default_context()
    with smtplib.SMTP(email_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(email_address, email_password)
        server.sendmail(email_address, reciever_email, message)
