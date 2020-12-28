import os
from email.message import EmailMessage
import smtplib
import time
from datetime import datetime
import ast
from dotenv import load_dotenv
from datetime import datetime,timedelta

try:
    load_dotenv(".env")
except:
    print(".env not found")

SENDER = os.environ.get("GMAIL_USER")
PASSWORD = os.environ.get("GMAIL_PASSWORD")
receivers=os.environ.get("RECEIVERS")
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

def generate_table(i=100,startdate=datetime(2020,12,28,17,0,0)):
    num_of_people=len(receiver)
    people=[[i%num_of_people,(i+1)%num_of_people] for i in range(i)]
    dumpname=[list(receiver.keys())[i[0]] for i in people]
    restorename=[list(receiver.keys())[i[1]] for i in people]
    dumpdate=[startdate+timedelta(days=7*i) for i in range(i)]
    restoredate=[startdate+timedelta(days=7*i+1) for i in range(i)]
    return dumpname,restorename,dumpdate,restoredate

def display(i,dumpname,restorename,dumpdate,restoredate):
    msg="Schedule next:\n\n"
    nearestindex=0
    now=datetime.now()
    timediff=now-dumpdate[nearestindex]
    closest="dump"
    closestindex=nearestindex
    while timediff.total_seconds()>0:
        nearestindex=nearestindex+1
        timediff=now-dumpdate[nearestindex]
    for ind in range(i):
        if nearestindex-1>0 and (now-restoredate[nearestindex-1]).total_seconds()>0:
            msg=msg+(restoredate[nearestindex-1]).strftime("%Y/%m/%d %H:%M:%S")+'\n'
            msg=msg+('Restore Transh bins: '+restorename[nearestindex-1]+'\n\n')
            closest="restore"
            closestindex=nearestindex-1
        msg=msg+(dumpdate[ind+nearestindex]).strftime("%Y/%m/%d %H:%M:%S")+'\n'
        msg=msg+('Dump Transh bins: '+dumpname[ind+nearestindex]+'\n\n')
        msg=msg+(restoredate[ind+nearestindex]).strftime("%Y/%m/%d %H:%M:%S")+'\n'
        msg=msg+('Restore Transh bins: '+restorename[ind+nearestindex]+'\n\n')
            
    return msg,closest,closestindex


now = datetime.now()
current_time = now.strftime("%Y/%m/%d %H:%M:%S")   
with open('log.txt','w') as file:
    file.write('Start service on '+current_time+'\n')
    file.close()
    print('Start service on '+current_time)

    
message={"dump":'Dump trash bins',"restore":'Restore trash bins'}

dumpname,restorename,dumpdate,restoredate=generate_table(100)
schedulenext,closest,closestindex=display(10,dumpname,restorename,dumpdate,restoredate)
    
if closest=="restore":
    nexttime=restoredate[closestindex]
    nextname=restorename[closestindex]
    time.sleep((nexttime-now).total_seconds())
    send_email(receiver[nextname],message["restore"],schedulenext)
    closestindex=closestindex+1
    
currentindex=closestindex
while currentindex<=len(dumpname):    
    now = datetime.now()
    nexttime=dumpdate[closestindex]
    nextname=dumpname[closestindex]
    time.sleep((nexttime-now).total_seconds())
    send_email(receiver[nextname],message["dump"],schedulenext)
    
    now = datetime.now()
    nexttime=restoredate[closestindex]
    nextname=restorename[closestindex]
    time.sleep((nexttime-now).total_seconds())
    send_email(receiver[nextname],message["restore"],schedulenext)
    
    currentindex=currentindex+1