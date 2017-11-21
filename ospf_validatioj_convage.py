import pexpect
import csv
import time 

usename = 'cisco'
password = 'cisco'
hostname = ['192.168.64.131','192.168.64.132','192.168.64.133']


for host in hostname:
	child = pexpect.spawn ('ssh ' + usename + '@' + host)
	child.expect('Password:')
	child.sendline(password)
	child.expect('>')
	child.sendline('ena')
	child.expect('Password:')
	child.sendline(password)
	child.expect('#')
	child.sendline('terminal length 0')
	child.expect('#')
	child.sendline('show ip route')
	child.expect('#')
	#print child.before

	if host == '192.168.64.131':
		if '2.2.2.2' in child.before and '3.3.3.3' in child.before:
			print host + " validated"
		else: 
			print host + " is not validated"

	elif host == '192.168.64.132':
		if '1.1.1.1' in child.before and '3.3.3.3' in child.before:
			print host + " validated"
		else: 
			print host + " is not validated"

	elif host == '192.168.64.133':
		if '2.2.2.2' in child.before and '1.1.1.1' in child.before:
			print host + " validated"
		else: 
			print host + " is not validated"
