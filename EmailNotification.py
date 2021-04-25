'''
The cons for this code is that editor has to figure out the carrier of each phone number
because different phone number has different MSS gateway domain

Tips:(the structure of user's phone#)
     phone number + MSS gateway domain
link(check out the domain): https://www.digitaltrends.com/mobile/how-to-send-a-text-from-your-email-account/
'''
import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = 'hackathonSend@gmail.com'
    msg['from']= user
    password = 'hackathon1230' #Go to https://myaccount.google.com.
                                  #Security > Turn on 2-Step Verification
                                  #Back to previous page and click"App passwords" to get a new specific password

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

if __name__ =='__main__':
    email_alert("Hey", "The order you subscribe is in stock","xxxxxxxxxx@mms.us.lycamobile.com") #email_alert("text", "text","user's phone number + carrier's domain")
    # xxxxxxxxxx@mms.us.lycamobile.com
    # xxxxxxxxxx@tmomail.net

'''
import smtplib

sender_email = "xxxxx@gmail.com"
password= input(str('enter your password'))
rec_email="xxxxxx@gmail.com"
messege = "In Stock Notify"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender_email,password)
print("success")
server.sendmail(sender_email,rec_email,messege)
print("sended")
'''
