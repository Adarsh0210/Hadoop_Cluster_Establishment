#!/usr/bin/python2

print "content-type:text/html"
print "\n"

from os import system 
import getpass
from commands import getstatusoutput
import mymodule
import thread
import cgi

#print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/configuring.html\">\n"

getstatusoutput("echo '127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1          localhost localhost.localdomain localhost6 localhost6.localdomain6\n' > /var/www/cgi-bin/hosts ")

#-------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
x=cgi.FormContent()
keys=x.keys()
ip=list()
fh=open("/var/www/cgi-bin/nmap2.txt","rw+")
for ips in fh:
	i=ips.strip()
	ip.append(i)
fh.close()

nip=0
sip=0
jip=0
hip=0
dnip=list()
ttip=list()
dnttip=list()
for items in keys:
	if items[0]=='a':
		nip=ip[int(items[1:])-1]
	elif items[0]=='b':
		sip=ip[int(items[1:])-1]
	elif items[0]=='c':
		jip=ip[int(items[1:])-1]
	elif items[0]=='d':
		l=int(items[1:])
		k=ip[l-1]
		dnip.append(k)
	elif items[0]=='e':
		l=int(items[1:])
		k=ip[l-1]
		ttip.append(k)
	elif items[0]=='f':
		l=int(items[1:])
		k=ip[l-1]
		dnttip.append(k)
	elif items[0]=='g':
		hip=ip[int(items[1:])-1]
#------------------------------------------------------------------------------------------------------	
#Stooping all services on these ips if any
num_thread=0
thread_started=False
lock=thread.allocate_lock()
def stop_service(ips):
	global num_thread,thread_started
	lock.acquire()
	thread_started=True
	num_thread+=1
	lock.release()
	x=getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} /usr/java/jdk1.7.0_79/bin/jps ".format(ips))			
	if "NameNode" in x[1]:
		getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop namenode ".format(ips))
	if "TaskTracker" in x[1]:
		getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop tasktracker".format(ips))
	if "JobTracker" in x[1]:
		getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop jobtracker".format(ips))
	if "DataNode" in x[1]:
		getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop datanode".format(ips))
	if "SecondaryNameNode" in x[1]:
		getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop secondarynamenode ".format(ips))
	lock.acquire()
	num_thread-=1
	lock.release()

def stop_services(i):
	global num_thread,thread_started
	for ips in i:
		thread.start_new_thread(stop_service,(ips,))
	while not thread_started:
		pass
	while num_thread > 0 :
		pass
	
stop_services(ip)
#----------------------------------------------------------------------------------------
getstatusoutput("echo '{}  nn ' >> /var/www/cgi-bin/hosts ".format(nip))	
getstatusoutput("echo '{}  jt ' >> /var/www/cgi-bin/hosts ".format(jip))
if sip!=0:
	getstatusoutput("echo '{}  snn ' >> /var/www/cgi-bin/hosts ".format(sip))
count=1
for ip in dnttip:
	getstatusoutput("echo '{0}  dntt{1} ' >> /var/www/cgi-bin/hosts ".format(ip,count))
	count+=1
count=1
for ip in dnip:
	getstatusoutput("echo '{0}  dn{1} ' >> /var/www/cgi-bin/hosts ".format(ip,count))
	count+=1
count=1
for ip in ttip:
	getstatusoutput("echo '{0}  tt{1} ' >> /var/www/cgi-bin/hosts ".format(ip,count))
	count+=1

getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hostnamectl set-hostname nn".format(nip))
getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hostnamectl set-hostname jt".format(jip))
if sip!=0:
	getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hostnamectl set-hostname snn".format(sip))
count=1
tt=1
dn=1
for i in ttip:
	getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} hostnamectl set-hostname tt{1}".format(i,tt))
	tt+=1

for i in dnip:
	getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hostnamectl set-hostname dn{}".format(i,dn))
	dn+=1

for i in dnttip:
	getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hostnamectl set-hostname dntt{}".format(i,count))
	count+=1

getstatusoutput("sudo \cp -f /var/www/cgi-bin/hosts /etc/hosts")
#Starting all the services
#-------------------------------------------------------------------------------------------------------------
def start_services():
	mymodule.start_namenode(nip,hip)
	mymodule.start_jobtracker(jip)
	if sip!=0:
		mymodule.start_secondarynamenode(sip)
	if len(dnip)>0:	
		mymodule.start_datanodes(dnip)
	if len(ttip)>0:		
		mymodule.start_tasktrackers(ttip)
	if len(dnttip)>0:	
		mymodule.start_datanodes(dnttip)
		mymodule.start_tasktrackers(dnttip)
		
start_services()

print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/H1userportal.html\">\n"
