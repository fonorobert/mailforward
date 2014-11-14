#!/usr/bin/env python3

import argparse
from configparser import ConfigParser

#Parse config
config = ConfigParser()
config.read('config.cfg')

#create a list of mailing lists from the config file

lists = []
for k, v in config['LISTS'].items():

    #strip whitespaces from email addresses
    this_list = v.split(',')
    new_list = []
    for a in this_list:
        new_list.append(a.strip())
    #append current list to list of all lists (yo dawg!)
    lists.append({k: new_list})


#Parse stdin
parser = argparse.ArgumentParser()
parser.add_argument('mail')

args = parser.parse_args()

with open('mailout.txt', mode='w', newline='') as f:
    print(args.mail, file=f)
