#!/usr/bin/python2


from os import system 
#import getpass
from commands import getstatusoutput
import mmymodule
import re
import thread
#-------------------------------------------------------------------------------------------------------------#

getstatusoutput("echo '127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1         localhost localhost.localdomain localhost6 localhost6.localdomain6' > /root/Desktop/Python/hosts ")

#-------------------------------------------------------------------------------------------------------------#
d1=dict()
d2=dict()
d3=dict()
def collect_ip():
	print "Enter the range of ip from which you want to scan"
	start=raw_input("Enter starting ip address : ").strip()
	end=raw_input("Enter end ip address : ").strip().split('.')
	#using nmap to collect the list of ips
	x=getstatusoutput("(nmap -sP {}-{} -n) >/di/nmap1.txt".format(start,end[3]))
	fhandle=open("/di/nmap1.txt","r+")
	fwrite=open("/di/nmap2.txt","w+")
	reg=re.compile(r"\b\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\b")
	lis=list()
	for lines in fhandle:
		mylis=reg.findall(lines)
		if len(mylis)>0:
			if mylis[0] not in lis:
				lis.append(mylis[0])
	excludeip=['192.168.43.53','192.168.43.13','192.168.43.110']	
	if lis[-1].split('.') not in lis[-2].split('.'):
		lis.remove(lis[-1])
	for items in range(1,len(lis)):
		if lis[items] not in excludeip:
			x1="cat /proc/meminfo | grep 'MemTotal:' | cut -f9 -d' ' "
			x2=" lscpu | grep 'CPU MHz:' | cut -f17 -d' '"
			x3=" df -hT | grep '/dev/mapper/rhel-root' | cut -f3 -d'G'" 
			x4="sshpass -p redhat ssh -o StrictHostKeyChecking=no -l root {0} \"{1};{2};{3}\"".format(lis[items],x1,x2,x3)
			x=getstatusoutput(x4)
			fwrite.write(lis[items])
			z=x[1].split('\n')			
			d1[lis[items]]=float(z[0])
			d2[lis[items]]=float(z[1])
			d3[lis[items]]=float(z[2])			
			fwrite.write(':')
			fwrite.write(z[0])
			fwrite.write(':')
			fwrite.write(z[1])
			fwrite.write(":")
			fwrite.write(z[2].strip()+'G')
			fwrite.write("\n")
	fhandle.close()
	fwrite.close()
collect_ip()

#-------------------------------------Writing in file--------------------------------------------#
lis=list()
fhandle=open("/di/nmap2.txt","r+")
system("tput setaf 1")
for lines in fhandle:
	line=lines.strip().split(':')
	lis.append(line[0])
	print "{}          {}           {}             {}".format(line[0],line[1],line[2],line[3])
print 
#--------------------------------stopping services if any--------------------------------------#
#Stooping all services on these ips if any
system("tput setaf 3")
print "PLEASE WAIT! STOPPING ALL SERVICES RUNNING ON YOUR SYSTEMS!"
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
			system("sshpass -p redhat ssh -l root {} hadoop-daemon.sh stop namenode ".format(ips))
	if "NodeManager" in (list(x)[1].strip().split()):
			system("sshpass -p redhat ssh -l root {} yarn-daemon.sh stop nodemanager".format(ips))
	if "ResourceManager" in (list(x)[1].strip().split()):
			system("sshpass -p redhat ssh -l root {} yarn-daemon.sh stop resourcemanager".format(ips))
	if "DataNode" in (list(x)[1].strip().split()):
			system("sshpass -p redhat ssh -l root {} hadoop-daemon.sh stop datanode".format(ips))
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
system("echo '{}  nn ' >> /di/hosts ".format(nip))	
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
system("echo '{}  jt ' >> /di/hosts ".format(jip))	
#-------------------------------------------------------------------------------------------------------------
#Setting up the hostname of each ip
system("sshpass -p redhat ssh -l root {} hostnamectl set-hostname nn".format(nip))
system("sshpass -p redhat ssh -l root {} hostnamectl set-hostname rm".format(jip))
count=1
for i in lis:
	system("echo '{}  dn-nm{} ' >> /di/hosts ".format(i,count))
	system("sshpass -p redhat ssh -l root {} hostnamectl set-hostname dn-nn{}".format(i,count))
	count+=1

#-------------------------------------------------------------------------------------------------------------
#Starting all the services

def start_services(nip,jip,lis):
	mmymodule.start_namenode(nip)
	mmymodule.start_resourcemanager(jip)
	mmymodule.start_dnnm(lis)
start_services(nip,jip,lis)					
