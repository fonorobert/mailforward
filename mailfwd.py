#!/usr/bin/env python3

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from configparser import ConfigParser
from email.utils import parseaddr

#function definitions


def readlist(input_file):
    with open(input_file, mode="r") as f:
        lines = f.readlines()
    result = [i.strip() for i in lines]
    return result


def bounce(bouncetext, incoming):
    msg = MIMEMultipart()
    msg['Subject'] = "Re: " + incoming['subject']
    msg['From'] = incoming['to']
    msg['To'] = incoming['from']
    msg.attach(MIMEText(bouncetext, _charset='UTF-8'))
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
    exit(0)


#Parse email

email_in = sys.stdin.read()

incoming = Parser().parsestr(email_in)

sender = incoming['from']
sender_str = parseaddr(sender)[1]
to_list = parseaddr(incoming['to'])[1]
list_user = to_list.split('@')[0]
this_address = incoming['to']

#Parse config
basedir = '/scripts/mailforward/'

config = ConfigParser()
config.read(basedir + 'config.cfg', encoding="utf-8")

senders_file = basedir + config['FILES']['senders']
noreply_raw = config['RULES']['noreply'].split(',')
bounce_text = config['MESSAGES']['bounce']
attachment_text = config['MESSAGES']['attachment']
nolist_text = config['MESSAGES']['nolist']
noreply = []
for addr in noreply_raw:
    noreply.append(addr.strip())

#Try to read list addresses based on original recipient, bounce if no list found

try:
    list_file = basedir + list_user + ".list"
except FileNotFoundError:
    bounce(nolist_text)

#Try to read senders list, fallback to globals if not found
try:
    senders_file = basedir + list_user + "_senders.list"
except FileNotFoundError:
    senders_file = basedir + config['FILES']['globalsenders']


#Read senders and recipients into lists

senders = readlist(senders_file)
list_members = readlist(list_file)

if sender_str not in senders:

    if sender_str in noreply:
        exit(0)
    else:
        bounce(bounce_text, incoming)

else:

    for member in list_members:
        msg = MIMEMultipart()
        msg.set_payload(incoming)
        msg['From'] = this_address
        msg['reply-to'] = sender
        msg['To'] = member
        msg['Subject'] = incoming['subject']

        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()
