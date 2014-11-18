#!/usr/bin/env python3
import io
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from configparser import ConfigParser
from email.utils import parseaddr

#email_in = sys.stdin.read()
input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
email_in = input_stream.read()

with open('mailout.txt', 'w') as f:
    f.write(email_in)

incoming = Parser().parsestr(email_in)

sender = incoming['from']
sender_str = parseaddr(sender)[1]
this_address = incoming['to']

if incoming.is_multipart():
    for payload in incoming.get_payload():
        # if payload.is_multipart(): ...
        body = payload.get_payload()
else:
    body = incoming.get_payload(decode=False)

type_body = type(body).__name__ + " " + type(body).__class__.__name__
type_all = type(incoming).__name__ + " " + type(incoming).__class__.__name__


msg = MIMEMultipart()
msg['Subject'] = incoming['subject']
msg['From'] = this_address
msg['To'] = sender
msg.attach(MIMEText(body + "\n" + type_body + "\n" + type_all, 'html', _charset='UTF-8'))

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
