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

email_in = sys.stdin.read()


def find_text(body_list):
    for payload in body_list:
        if len(payload) == 1:
            if type(payload) == str:
                body = payload
                return body
            else:
                body = payload.get_payload(decode=True)
                body = body.decode('utf-8')
                return body
        else:
            find_text(payload)



incoming = Parser().parsestr(email_in)

sender = incoming['from']
sender_str = parseaddr(sender)[1]
this_address = incoming['to']

if incoming.is_multipart():
    for payload in incoming.get_payload():
        # if payload.is_multipart(): ...
        body = payload.get_payload(decode=True)
        body = body.decode('utf-8')

    # body_list = incoming.get_payload()
    # body = find_text(body_list)

    # try:
    #     if body is "":
    #         body = "Erre  listára nem küldhet csatolt fájlokat."
    # except NameError:
    #     body = "Erre  listára nem küldhet csatolt fájlokat." + body_list[0].get_content_type() + str(body_list[0].keys()) + str(body_list[1].keys()) + "/n" + types


    # for payload in incoming.get_payload():
    #     # if payload.is_multipart(): ...
    #     body = payload.get_payload(decode=True)
    #     #body = body.decode('utf-8')
    #     body = str(body.keys())
else:
    body = incoming.get_payload(decode=True)
    body = body.decode('utf-8')

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
