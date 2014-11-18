#!/usr/bin/env python3
import os
import pwd
import io
import sys
import smtplib
import codecs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
from configparser import ConfigParser
from email.utils import parseaddr

#email_in = sys.stdin.read()
input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
email_in = input_stream.read()
#email_in = base64.b64decode(email_in).decode('utf-8')

# email_in = email_in.encode()
# email_in = codecs.decode(email_in, 'base64')
# email_in = email_in.decode('utf-8', 'replace')


def get_username():
    return pwd.getpwuid(os.getuid())[0]

running_user = get_username()
# with open('mailout.txt', 'w') as f:
#     f.write(email_in)

incoming = Parser().parsestr(email_in)

sender = incoming['from']
sender_str = parseaddr(sender)[1]
this_address = incoming['to']

if incoming.is_multipart():
    body_list = incoming.get_payload()

    # for payload in body_list:
    #     if payload.get('Content-Type') is not

    if len(body_list) is 1:
        body = body_list[0].get_payload(decode=True)
        body = body.decode('utf-8')
    else:
        body = "Erre  listára nem küldhet csatolt fájlokat." + body_list[0].get_content_type() + str(len(body_list)) + str(body_list[0].keys()) + str(body_list[1].keys())
    # body = ""
    # for payload in body_list:
    #     body = body + str(payload.keys())

    #body = body + body_list[1].get('Content-Disposition')

    #body = str(body.keys())

    # for payload in incoming.get_payload():
    #     # if payload.is_multipart(): ...
    #     body = payload.get_payload(decode=True)
    #     #body = body.decode('utf-8')
    #     body = str(body.keys())
else:
    body = incoming.get_payload(decode=True)
    body = body.decode('utf-8')
    # body = body.encode()
    # body = codecs.decode(body, 'base64')
    # body = body.decode('utf-8', 'replace')

type_body = type(body).__name__ + " " + type(body).__class__.__name__
type_all = str(incoming.get_charsets())
type_in = type(email_in).__name__


msg = MIMEMultipart()
msg['Subject'] = incoming['subject']
msg['From'] = this_address
msg['To'] = sender
msg.attach(MIMEText(body, 'html', _charset='UTF-8'))

#msg.set_charset('utf-8')
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
