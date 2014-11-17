#!/usr/bin/env python3

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

#function to read address lists into list


def readlist(input_file):
    with open(input_file, mode="r") as f:
        lines = f.readlines()
    result = [i.strip() for i in lines]
    return result

email_in = sys.stdin.read()

incoming = Parser().parsestr(email_in)

sender = incoming['from']
sender_str = parseaddr(sender)[1]
me = incoming['to']

senders = readlist("/home/fonorobert/scripts/mailforward/senders.list")

if incoming.is_multipart():
    for payload in incoming.get_payload():
        # if payload.is_multipart(): ...
        body = payload.get_payload()
else:
    body = incoming.get_payload()


if sender_str not in senders:
    msg = MIMEMultipart()
    msg['Subject'] = "Re: " + incoming['subject']
    msg['From'] = me
    msg['To'] = sender
    msg.attach(MIMEText("Önnek nincs jogosultsága üzenetet küldeni erre a címre.",'html'))
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

else:
    list_members = readlist("/home/fonorobert/scripts/mailforward/madrich.list")

    for member in list_members:
        msg = MIMEMultipart()
        msg['Subject'] = incoming['subject']
        msg['From'] = me
        msg['To'] = member
        msg.attach(MIMEText(body, 'html'))
        
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()
