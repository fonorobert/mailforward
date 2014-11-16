#!/usr/bin/env python3

import sys
import smtplib
from email.mime.text import MIMEText
from email.parser import Parser
import email

#function to read address lists into list


# def readlist(file):
#     with open(file, mode="r") as f:
#         lines = f.readlines()
#     result = [i.strip() for i in lines]
#     return result

email_in = sys.stdin.read()

headers = Parser().parsestr(email_in)

sender = headers['from']
me = headers['to']

msg = MIMEText('deőfjőwejf')

msg['Subject'] = headers['subject']
msg['From'] = me
msg['To'] = sender

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
