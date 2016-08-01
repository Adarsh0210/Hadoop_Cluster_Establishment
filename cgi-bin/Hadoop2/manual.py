#!/usr/bin/python2

#This program is for manual comfiguration of hadoop cluster

from commands import getstatusoutput
import mymodule
import thread
import cgi
print "content-type:text/html"
print "\n"

#-------------------------------------------------------------------------------------------------------------#

getstatusoutput("echo '127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1         localhost localhost.localdomain localhost6 localhost6.localdomain6' > /var/www/cgi-bin/hosts ")

#-------------------------------------------------------------------------------------------------------------#
x=cgi.FormContent()
keys=x.keys()
#print x
ip=list()
fh=open("/var/www/cgi-bin/nmap2.txt","rw+")
for ips in fh:
	i=ips.strip()
	ip.append(i)
fh.close()

nip=0
rip=0
dnip=list()
nmip=list()
dnnmip=list()
#keys=['b1','e2','e3','a4']
for items in keys:
	if items[0]=='a':
		nip=ip[int(items[1:])-1]
	elif items[0]=='b':
		rip=ip[int(items[1:])-1]
	elif items[0]=='c':
		l=int(items[1:])
		k=ip[l-1]
		dnip.append(k)
	elif items[0]=='d':
		l=int(items[1:])
		k=ip[l-1]
		nmip.append(k)
	elif items[0]=='e':
		l=int(items[1:])
		k=ip[l-1]
		dnnmip.append(k)
#print ip

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
	x=getstatusoutput("sshpass -p redhat ssh -l root {} jps ".format(ips))			
	if "NameNode" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -l root {} hadoop-daemon.sh stop namenode ".format(ips))
	if "ResourceManager" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -l root {} yarn-daemon.sh stop resourcemanager".format(ips))
	if "NodeManager" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -l root {} yarn-daemon.sh stop nodemanager".format(ips))
	if "DataNode" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -l root {} hadoop-daemon.sh stop datanode".format(ips))
	lock.acquire()
	num_thread-=1
	lock.release()

def stop_services(ip):
	global num_thread,thread_started
	for ips in ip:
		thread.start_new_thread(stop_service,(ips,))
	while not thread_started:
		pass
	while num_thread > 0 :
		pass
		
stop_services(ip)
#------------------------------------------------------------------------------------------------------------

#setting all the respective services......

getstatusoutput("echo '{}  nn ' >> /var/www/cgi-bin/hosts ".format(nip))	
getstatusoutput("echo '{}  rm ' >> /var/www/cgi-bin/hosts ".format(rip))
count=1
for ip in dnnmip:
	getstatusoutput("echo '{0}  dnnm{1} ' >> /var/www/cgi-bin/hosts ".format(ip,count))
	count+=1
count=1
for ip in dnip:
	getstatusoutput("echo '{0}  dn{1} ' >> /var/www/cgi-bin/hosts ".format(ip,count))
	count+=1
count=1
for ip in nmip:
	getstatusoutput("echo '{0}  nm{1} ' >> /var/www/cgi-bin/hosts ".format(ip,count))
	count+=1


getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} hostnamectl set-hostname nn".format(nip))
getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} hostnamectl set-hostname rm".format(rip))
count=1
tt=1
dn=1
for i in nmip:
	getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} hostnamectl set-hostname nm{1}".format(i,tt))
	tt+=1

for i in dnip:
	getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} hostnamectl set-hostname dn{1}".format(i,dn))
	dn+=1

for i in dnnmip:
	getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} hostnamectl set-hostname dnnm{1}".format(i,count))
	count+=1

getstatusoutput("sudo \cp -f  /var/www/cgi-bin/hosts /etc/hosts")

#Starting all the services
#-------------------------------------------------------------------------------------------------------------
def start_services():
	mymodule.start_namenode(nip)
	mymodule.start_resourcemanager(rip)
	if len(dnip)>0:	
		mymodule.start_datanodes(dnip)
	if len(nmip)>0:		
		mymodule.start_nodemanager(nmip)
	if len(dnnmip)>0:	
		mymodule.start_dnnm(dnnmip)
		
		
start_services()					

print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/H2userportal.html\">\n"
