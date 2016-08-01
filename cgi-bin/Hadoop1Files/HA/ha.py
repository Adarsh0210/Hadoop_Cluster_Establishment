#!/usr/bin/python2

import time
from os import system
from commands import getstatusoutput

def namenode(nip,anip,flag):
    getstatusoutput("ifconfig enp0s8 {}".format(nip))
    getstatusoutput("hostnamectl set-hostname nn")
    getstatusoutput("hadoop-daemon.sh start namenode")
    if flag==2:
	getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} 'init 0' ".format(anip))
                
def ha(anip,nip):
	while True:
	        x=getstatusoutput("ping -c 1 {}".format(anip))
		if "Destination Host Unreachable" in x[1]:
                    namenode(nip,anip,1)
	            break
                y=getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} /usr/java/jdk1.7.0_79/bin/jps".format(anip))            
		if "NameNode" not in y[1]:
	            namenode(nip,anip,2)
                    break


ha('192.100.64.2','192.168.43.11')                        
