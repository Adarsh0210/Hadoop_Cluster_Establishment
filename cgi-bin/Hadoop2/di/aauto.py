#!/usr/bin/python2

print "content-type:text/html\n"

from os import system 
#import getpass
from commands import getstatusoutput
import mmymodule
import thread
import cgi,cgitb
cgitb.enable()
#-------------------------------------------------------------------------------------------------------------#

getstatusoutput("echo '127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1         localhost localhost.localdomain localhost6 localhost6.localdomain6' > /var/www/cgi-bin/hosts ")

#-------------------------------------------------------------------------------------------------------------#

d1=dict()
d2=dict()
d3=dict()
def collect_ip(start,end):
	x=getstatusoutput("nmap -sP {}-{} -n | grep 'Nmap scan'| cut -f5 -d' ' > /var/www/cgi-bin/nmap1.txt".format(start,end[3]))
	fhandle=open("/var/www/cgi-bin/nmap1.txt","r+")
	fwrite=open("/var/www/cgi-bin/nmap2.txt","w+")
	lis=list()
	for lines in fhandle:
		lis.append(lines)
	excludeip=['192.168.43.2','192.168.43.1','192.168.43.110','192.168.43.53','192.168.43.4','192.168.43.12']	
	count=0
	for items in lis:
		items=items.strip()
		if items not in excludeip:
			x1="cat /proc/meminfo | grep 'MemTotal:' | cut -f9 -d' ' "
			x2=" lscpu | grep 'CPU MHz:' | cut -f17 -d' '"
			x3=" df -hT | grep '/dev/mapper/rhel-root' | cut -f10 -d' '" 
			x4="sshpass -p redhat ssh -o StrictHostKeyChecking=no -l root {0} \" {1}; {2}; {3}\"".format(items,x1,x2,x3)
			x=getstatusoutput(x4)
			z=x[1].split('\n')
			d1[items]=float(z[0])
			d2[items]=float(z[1])
			d3[items]=float(z[2].strip('G'))
			fwrite.write(items)			
			fwrite.write(':')
			fwrite.write(z[0])
			fwrite.write(':')
			fwrite.write(z[1])
			fwrite.write(":")
			fwrite.write(z[2])
			fwrite.write("\n")
	fhandle.close()
	fwrite.close()

x=cgi.FormContent()
start=x['START'][0]
end=x['END'][0]
start=start.strip()
end=end.strip().split('.')
collect_ip(start,end)

#-------------------------------------Writing in file--------------------------------------------#
lis=list()
fhandle=open("/var/www/cgi-bin/nmap2.txt","r+")
#getstatusoutput("tput setaf 1")
for lines in fhandle:
	line=lines.strip().split(':')
	lis.append(line[0])
#--------------------------------stopping services if any--------------------------------------#
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
	x=getstatusoutput("sshpass -p redhat ssh -l root {} /usr/java/jdk1.7.0_79/bin/jps ".format(ips))			
	if "NameNode" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -l root {} hadoop-daemon.sh stop namenode ".format(ips))
	if "NodeManager" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -l root {} yarn-daemon.sh stop nodemanager".format(ips))
	if "ResourceManager" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -l root {} yarn-daemon.sh stop resourcemanager".format(ips))
	if "DataNode" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -l root {} hadoop-daemon.sh stop datanode".format(ips))
	lock.acquire()
	num_thread-=1
	lock.release()

def stop_services(lis):
	global num_thread,thread_started
	for ips in lis:
		thread.start_new_thread(stop_service,(ips,))
	while not thread_started:
		pass
	while num_thread > 0 :
		pass
		
stop_services(lis)	

#------------------------------------------------------------------------------------------------------------
#This part is to take ip of namenode
#maxv=0
#temp=0
flag=0
for i in lis:
	if flag == 0:
		maxv=d1[i]*0.55+d2[i]*0.30+d3[i]*0.15
		nip=i
		flag=1
	else:
		temp=d1[i]*0.55+d2[i]*0.30+d3[i]*0.15
		if temp > maxv:
			maxv=temp
			nip=i

lis.remove(nip)
getstatusoutput("echo '{}  nn ' >> /var/www/cgi-bin/hosts".format(nip))	
#sortedip.remove(nip)

#-------------------------------------------------------------------------------------------------------------
#This part is to take ip of resourcemanager
jflag=0
for i in lis:
	if jflag == 0:
		maxv=d1[i]*0.40+d2[i]*0.55+d3[i]*0.05
		jip=i
		jflag=1
	else:
		temp=d1[i]*0.40+d2[i]*0.55+d3[i]*0.05
		if temp > maxv:
			maxv=temp
			jip=i

lis.remove(jip)
getstatusoutput("echo '{}  rm ' >> /var/www/cgi-bin/hosts ".format(jip))	
#-------------------------------------------------------------------------------------------------------------
#Setting up the hostname of each ip
getstatusoutput("sshpass -p redhat ssh -l root {} hostnamectl set-hostname nn".format(nip))
getstatusoutput("sshpass -p redhat ssh -l root {} hostnamectl set-hostname rm".format(jip))
count=1
for i in lis:
	getstatusoutput("echo '{}  dnnm{} ' >> /var/www/cgi-bin/hosts ".format(i,count))
	getstatusoutput("sshpass -p redhat ssh -l root {} hostnamectl set-hostname dnnm{}".format(i,count))
	count+=1

#-------------------------------------------------------------------------------------------------------------
#Starting all the services
getstatusoutput("sudo \cp -f  /var/www/cgi-bin/hosts /etc/hosts")

def start_services(nip,jip,lis):
	mmymodule.start_namenode(nip)
	mmymodule.start_resourcemanager(jip)
	mmymodule.start_dnnm(lis)
start_services(nip,jip,lis)

print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/H2userportal.html\">\n"
