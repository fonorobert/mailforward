#!/usr/bin/env python3

#import argparse
import sys
from configparser import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.parser import Parser

#Parse config
config = ConfigParser()
config.read('config.cfg')

email_in = sys.stdin.read()


#with open('mailout.txt', mode='w', newline='') as f:
#    print(args, file=f)

headers = Parser().parsestr(email_in)
sender = headers['from']
me = headers['to']

msg = MIMEText('Teszt üzenet')

msg['Subject'] = headers['subject']
msg['From'] = me
msg['To'] = 'teszt.fonorobert@gmail.com'

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
