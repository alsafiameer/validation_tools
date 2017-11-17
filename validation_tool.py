#!/usr/bin/env python
"""
ASSUMPTIONS:
=============
1- yaml file will use as var file, jinja2 template will use as template !
2- you need to install python pip and python's modules like pexpect,jinja2

PYTHON PIP: https://pypi.python.org/pypi/pip 
PEXPECT MO.: http://pexpect.readthedocs.io/en/stable/ 
JINJA2 TEMPLATE MO.: http://jinja.pocoo.org/docs/2.10/ 


WORKING: 
========
1- clone it. 
2- chmod +x validation_tool.py 

how to run it: 
./validation_tool.py <HOSTNAME> <VAR_FILE(YML)>

"""

import pexpect
import getpass
import sys
import yaml
import time 
from sys import argv
from jinja2 import Template


script, hostname, var = argv 


def connect_to_app(hostname): 
	password = getpass.getpass("Enter your account password ")
	conct_sw = pexpect.spawn ('ssh ' + hostname) 
	out_put = conct_sw.expect (["(yes/no)" , "password: "])
	if out_put == 0: 
		conct_sw.send("yes")

		conct_sw.expect("password: ")
		conct_sw.send(password)
		print "Logging to " + hostname 
	elif out_put == 1:
		conct_sw.send(password) 
	else: 
		print " Switch is unreachable!" 

#this one send_comands_to_sw should modify with expected/push configs!
def send_comands_to_sw(conf_file): 
	while True: 
		print "Opning config file! " 
		with open (conf_file , 'r') as f: 
			for line in f: 
				print line,
				print_line = raw_input ("Enter 'y' for print, 'n' to skip or 'qu' to exit > ")
				if print_line == "y" or print_line == "Y" : 
					print line.strip() + "\n"
				elif print_line == "n" or print_line == "N" :
					print " You dont need to print line " + line 
					pass
				elif print_line == "qu": 
					exit()
				else: 
					print " Worng input!"
		f.close()
	return 

"""
load both yml file and template and create config file. 
"""

datavars = yaml.load(open(var).read())
template = Template(open("config_temp.j2").read())
readoutput = template.render(datavars)
saveconfigs = open(var + "_conf" , "w")
saveconfigs.write(readoutput)
saveconfigs.write("\n")
saveconfigs.close()

print "configuration has been creat! "

""" 
will propate the user to choose if he/sh needs to excude the comands, then connect to host by using connect_to_app() after that used send_comands_to_sw() to excude the comand with interction and skip option 
"""
while True: 
	ex_config = raw_input ("Type 'y' to excude the configs and 'n' to abort > ") 
	if ex_config == "y": 
		config_file = "config_" + var
		connect_to_app(hostname)
		send_comands_to_sw(config_file) 
	else: 
		exit()
