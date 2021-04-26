import smtplib
from email.message import EmailMessage


def email_alert (subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to']= to

    user = 'hackathonSend@gmail.com'
    msg['from']= user
    password = 'hackathon1230'

    server = smtplib.SMTP ('smtp.gmail.com',587)
    server.starttls()
    server.login (user, password)
    server.send_message(msg)

    server.quit()


if __name__ == '__main__' :
    email_alert("Notify", "The product is in stock", "xxxxxx.gmail.com")
