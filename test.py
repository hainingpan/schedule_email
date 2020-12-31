import os
from email.message import EmailMessage
import smtplib
import time
from datetime import datetime
import ast
# from dotenv import load_dotenv
from datetime import datetime,timedelta

try:
    env={}
    with open(".env") as credentials:
        for line in credentials:
            name, var = line.partition("=")[::2]
            env[name.strip()] = var.replace('\n','')
except:
    print(".env not found")

SENDER = env["GMAIL_USER"]
PASSWORD = env["GMAIL_PASSWORD"]
receivers=env["RECEIVERS"]
receiver = ast.literal_eval(receivers)


def send_email(recipient, subject, body,time=True,filename='log.txt'):
    now = datetime.now()
    current_time = now.strftime("%Y/%m/%d %H:%M:%S")
    msg = EmailMessage()
    msg.set_content(body+('\nsent at '+current_time )*(time==True))
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = recipient
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    server.quit()
    with open(filename,'a') as file:
        text=current_time+' sent to '+recipient+'\n'
        file.write(text)
        file.close()

for i in range(3):
    send_email('jackpan1994@gmail.com',SENDER,'test')
    time.sleep(10)
