#!/usr/bin/python2

from os import system
from commands import getstatusoutput
def install(ip):
	print "Installing and configuring hadoop 2 on your system"
	system("sshpass -p redhat scp -r /root/Desktop/Hadoop2/SOFT/hadoop-2.6.4.tar.gz root@{}:/ ".format(ip))
	c="cd /"
	i="tar -xzf hadoop-2.6.4.tar.gz"
	m="mv hadoop-2.6.4 /hadoop2"
	system("sshpass -p redhat ssh -l root {} \"{};{};{}\"".format(ip,c,i,m))
	system("sshpass -p redhat scp -r /root/Desktop/Hadoop2/ConfigurationFiles/.bashrc root@{}:/root/ ".format(ip))

def localConfig():
	print "Enter the IP address on which you want to establish the local cluster"
	ip=raw_input("IP :- ")
	cmd="hadoop version | grep Hadoop | cut -f2 -d' '"
	x=getstatusoutput("sshpass -p redhat ssh -l root {} {}".format(ip,cmd))
	if x[1]=='':
		install(ip)
		x=getstatusoutput("sshpass -p redhat ssh -l root {} {}".format(ip,cmd))
		print x[1]	
		raw_input()
	elif x[1]=='1.2.1':
		system("sshpass -p redhat ssh -l root {} yum remove hadoop -y".format(ip,c,i,m))
		install(ip)

		
			

localConfig()	
