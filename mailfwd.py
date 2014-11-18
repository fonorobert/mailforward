#!/usr/bin/env python3

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from configparser import ConfigParser
from email.utils import parseaddr


#Parse config
config = ConfigParser()
config.read('/home/fonorobert/scripts/mailforward/config.cfg')
list_file = config['FILES']['list']
senders_file = config['FILES']['senders']
noreply_raw = config['RULES']['noreply'].split(',')
noreply = []
for addr in noreply_raw:
    noreply.append(addr.strip())


#function to read address lists into list


def readlist(input_file):
    with open(input_file, mode="r") as f:
        lines = f.readlines()
    result = [i.strip() for i in lines]
    return result

email_in = sys.stdin.read()

incoming = Parser().parsestr(email_in)
type_all = type(incoming)

sender = incoming['from']
sender_str = parseaddr(sender)[1]
this_address = incoming['to']

senders = readlist(senders_file)

if incoming.is_multipart():
    for payload in incoming.get_payload():
        # if payload.is_multipart(): ...
        body = payload.get_payload()
else:
    body = incoming.get_payload(decode=True)

type_body = type(body)
if sender_str not in senders:
    
#    if sender_str in noreply:
        #exit(0)

    
    msg = MIMEMultipart()
    msg['Subject'] = "Re: " + incoming['subject']
    msg['From'] = this_address
    msg['To'] = sender
    msg.attach(MIMEText("Önnek nincs jogosultsága üzenetet küldeni erre a címre." + type_all + type_body,'html', _charset='UTF-8'))
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

else:
    list_members = readlist(list_file)

    for member in list_members:
        msg = MIMEMultipart()
        msg['Subject'] = incoming['subject']
        msg['From'] = this_address
        msg['reply-to'] = sender
        msg['To'] = member
        msg.attach(MIMEText(body.encode('utf-8'), 'html', _charset='UTF-8'))

        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()
