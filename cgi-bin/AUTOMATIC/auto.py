#!/usr/bin/python2

print "content-type:text/html"
print ""

from os import system 
from commands import getstatusoutput
import mymodule
import thread
import cgi

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
#	print "{}          {}           {}             {}".format(line[0],line[1],line[2],line[3])
#print 
#--------------------------------stopping services if any--------------------------------------#
#Stooping all services on these ips if any
#print "PLEASE WAIT! STOPPING ALL SERVICES RUNNING ON YOUR getstatusoutputS!"
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
	if "NameNode" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop namenode ".format(ips))
	if "TaskTracker" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop tasktracker".format(ips))
	if "JobTracker" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop jobtracker".format(ips))
	if "DataNode" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop datanode".format(ips))
	if "SecondaryNameNode" in (list(x)[1].strip().split()):
			getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hadoop-daemon.sh stop secondarynamenode ".format(ips))
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
flag=0
for i in lis:
	if flag == 0:
		maxv=d1[i]*0.60+d2[i]*0.25+d3[i]*0.15
		nip=i
		flag=1
	else:
		temp=d1[i]*0.60+d2[i]*0.25+d3[i]*0.15
		if temp > maxv:
			maxv=temp
			nip=i
	
lis.remove(nip)
flag=0
for i in lis:
	if flag == 0:
		maxv=d1[i]*0.55+d2[i]*0.30+d3[i]*0.15
		hip=i
		flag=1
	else:
		temp=d1[i]*0.55+d2[i]*0.30+d3[i]*0.15
		if temp > maxv:
			maxv=temp
			ip=i
							
			
lis.remove(hip)

#-------------------------------------------------------------------------------------------------------------
#This part is to take ip of jobtracker
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

#-----------------------------------------------------------------------------------------
#This part is to take ip of secondarynamenode
sflag=0
for ip in lis:
	if sflag == 0:
		maxv=d1[ip]*0.34+d2[ip]*0.33+d3[ip]*0.33
		sip=ip
		sflag=1
	else:
		temp=d1[ip]*0.34+d2[ip]*0.33+d3[ip]*0.33
		if temp > maxv:
			maxv=temp
			sip=ip

lis.remove(sip)

#-------------------------------------------------------------------------------------------------------------
#This part is to set ips of namenode jobtracker and secondarynamenode in hostsfile
getstatusoutput("echo '{}  nn ' >> /var/www/cgi-bin/hosts ".format(nip))	
getstatusoutput("echo '{}  jt ' >> /var/www/cgi-bin/hosts ".format(jip))
getstatusoutput("echo '{}  snn ' >> /var/www/cgi-bin/hosts ".format(sip))

#-------------------------------------------------------------------------------------------------------------


#Setting up the hostname of each ip
getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hostnamectl set-hostname nn".format(nip))
getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hostnamectl set-hostname jt".format(jip))
getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hostnamectl set-hostname snn".format(sip))
count=1
for i in lis:
	getstatusoutput("echo '{}  dntt{} ' >> /var/www/cgi-bin/hosts ".format(i,count))
	getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} hostnamectl set-hostname dntt{}".format(i,count))
	count+=1

#-------------------------------------------------------------------------------------------------------------
#Starting all the services
getstatusoutput("sudo \cp -f  /var/www/cgi-bin/hosts /etc/hosts")

def start_services(nip,jip,snn,lis,hip):
	mymodule.start_namenode(nip,hip)
	mymodule.start_jobtracker(jip)
	mymodule.start_secondarynamenode(snn)
	mymodule.start_datanodes(lis)
	mymodule.start_tasktrackers(lis)

start_services(nip,jip,sip,lis,hip)

print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/H1userportal.html\">\n"
