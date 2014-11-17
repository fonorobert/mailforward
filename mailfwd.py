#!/usr/bin/env python3

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser

#function to read address lists into list


# def readlist(file):
#     with open(file, mode="r") as f:
#         lines = f.readlines()
#     result = [i.strip() for i in lines]
#     return result

email_in = sys.stdin.read()

incoming = Parser().parsestr(email_in)

sender = incoming['from']
me = incoming['to']

if incoming.is_multipart():
    for payload in incoming.get_payload():
        # if payload.is_multipart(): ...
        body = payload.get_payload()
else:
    body = incoming.get_payload()


msg = MIMEMultipart()

msg['Subject'] = incoming['subject']
msg['From'] = me
msg['To'] = sender

msg.attach(MIMEText(body, 'plain'))

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
