#!/usr/bin/python2

#This program is for automatic comfiguration of hadoop cluster

from os import system 
import getpass
from commands import getstatusoutput
import mymodule
import thread
#-------------------------------------------------------------------------------------------------------------#

getstatusoutput("echo '127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1         localhost localhost.localdomain localhost6 localhost6.localdomain6' > /root/Desktop/Python/hosts ")

#-------------------------------------------------------------------------------------------------------------#
def collect_ip():
	print "Enter the range of ip from which you want to scan"
	start=raw_input("Enter starting ip address : ").strip()
	end=raw_input("Enter end ip address : ").strip().split('.')
	#using nmap to collect the list of ips
	x=getstatusoutput("nmap -sP {}-{} -n | grep 'Nmap scan'| cut -f5 -d' ' > /di/nmap1.txt".format(start,end[3]))
	fhandle=open("/di//nmap1.txt","r+")
	fwrite=open("/di/nmap2.txt","w+")
	lis=list()
	for lines in fhandle:
		print lines		
		lis.append(lines)
	print lis	
#	print "Enter the list of IP's one by one which you want to exclude from the cluster , Enter 1 to terminate"
	
	excludeip=list()
#	while True:
#		ip=raw_input("Enter :")
#		if ip=="1":
#			break
#		excludeip.append(ip)
	
	excludeip=["192.168.43.1","192.168.43.53","192.168.43.2","192.168.43.110","192.168.43.192","192.168.43.168","192.168.43.118"]
#	if lis[-1].split('.') not in lis[-2].split('.'):
#		lis.remove(lis[-1])
	for items in lis:
		items=items.strip()
		if items not in excludeip:
			x1="cat /proc/meminfo | grep 'MemTotal:' | cut -f9 -d' ' "
			x2=" lscpu | grep 'CPU MHz:' | cut -f17 -d' '"
			x3=" df -hT | grep '/dev/mapper/rhel-root' | cut -f3 -d'G'" 
			x4="sshpass -p redhat ssh -o StrictHostKeyChecking=no -l root {0} \"{1};{2};{3}\"".format(items,x1,x2,x3)
			x=getstatusoutput(x4)
			fwrite.write(items)
			z=x[1].split('\n')
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

#-----------------------------------------------------------------------------------------------------------

system("clear")
#system("tput setaf 1")
# print "\t\t\tWELCOME TO MANUAL CONFIGURATION OF HADOOP2 CLUSTER \n"
#system("tput setaf 2")
#print "\t\t---------------------------------------------------------------"
#system("tput setaf 4")
#pas=getpass.getpass("\nENTER PASSWORD TO AUTHENTICATE YOURSELF!")
#if pas!="redhat":
#	print "UNAUTHORISED PERSON ACCESS! TAKING SECURITY MEASURE.\n\t\t<<TERMINATING PROGRAM>>\n"
#	system("sleep 2")	
#	exit()
lis=list()
ipram=dict()
fhandle=open("/di/nmap2.txt","r+")
system("tput setaf 1")
print "The list of Systems along with there specifications is shown below which are connected to uour network"
print "I.P ADDRESS            RAM           CPU MHz            FREE DISK SAPCE"	
for lines in fhandle:
	line=lines.strip().split(':')
	ipram[line[0]]=line[1]		
	print "{}          {}           {}             {}".format(line[0],line[1],line[2],line[3])
system("tput setaf 6")
print 
sortedip=sorted(ipram,key=ipram.get)
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
			system("sshpass -p redhat ssh -l root {} hadoop-daemon.sh stop namenode ".format(ips))
	if "ResourceManager" in (list(x)[1].strip().split()):
			system("sshpass -p redhat ssh -l root {} yarn-daemon.sh stop resourcemanager".format(ips))
	if "NodeManager" in (list(x)[1].strip().split()):
			system("sshpass -p redhat ssh -l root {} yarn-daemon.sh stop nodemanager".format(ips))
	if "DataNode" in (list(x)[1].strip().split()):
			system("sshpass -p redhat ssh -l root {} hadoop-daemon.sh stop datanode".format(ips))
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
		
stop_services(sortedip)
#------------------------------------------------------------------------------------------------------------
#This part is to take ip of namenode	
nip=raw_input("Enter an IP address for the 'namenode' from above shown list : ")
if nip not in sortedip:
	print "Invalid ip choice! Choosing ip address according to highest ram available"
	print "IP for NameNode choosen is {}".format(sortedip[-1])
	nip=sortedip[-1]
	print sortedip[-1]	
	system("echo '{}  nn ' >> /di//hosts ".format(sortedip[-1]))	
        sortedip.remove(sortedip[-1])
else:
	system("echo '{}  nn ' >> /di/hosts ".format(nip))	
	sortedip.remove(nip)

#This part is to take ip of resourcemanager	
#-------------------------------------------------------------------------------------------------------------
rip=raw_input("Enter an IP address for the 'resourcemanager' from above shown list : ")
if rip not in sortedip:
	print "Invalid ip choice or ip being used! Choosing ip address according to highest ram available"
	print "IP for 'resourcemanager' choosen is {}".format(sortedip[-1])
	system("echo '{}  rm ' >> /di/hosts ".format(sortedip[-1]))	
	rip=sortedip[-1]	
	sortedip.remove(sortedip[-1])		
else:
	system("echo '{}  rm ' >> /di/hosts ".format(rip))	
	sortedip.remove(rip)

#This part is to take ip of datanodes and nodemanager
#-------------------------------------------------------------------------------------------------------------
ddflag=dflag=nmflag=flag=0
dnlist=list()
nmlist=list()
print "Do you want to have all datanodes and nodemanager s on same commodity hardware?"
ch=raw_input("Enter 'yes' or 'no' without quotes : ")
if ch=="yes":
	flag=1
        no=int(raw_input("How many datanode and nodemanager you want to have in your cluster ?"))
        if no > len(sortedip) :
	        print "You dont have that much commodity hardwares! Enter value less than {}".format(len(sortedip))
	        no=int(raw_input("How  datanode and nodemanager you want to have in your cluster ?"))
	        if no > len(sortedip):
			dflag=1      
			print "Making all the left over commodity hardwares as datanodes and nodemanager"
			dnlist=sortedip[:]
			nmlist=sortedip[:]
	        else:
			dflag=2			
	                listip=list()
		        listip=[raw_input("Enter ip one by one") for i in range(no)]
		        listip=[item for item in listip if item in sortedip]
			dnlist=listip[:]
			nmlist=listip[:]
else:
#-------------------------------------------------------------------------------------------------------------
#For datanode
        no=int(raw_input("How many datanode you want to have in your cluster ?"))
        if no > len(sortedip) :
	        print "You dont have that much commodity hardwares! Enter value less than {} : ".format(len(sortedip))
	        no=int(raw_input("How many datanode you want to make ?  "))
	        if no > len(sortedip) :
			ddflag=1		        
			print "Making all the left over commodity hardwares as datanodes"
			dnlist=sortedip[:]
	        else:
			ddflag=2	                
        	        listip=list()
		        listip=[raw_input("Enter ip one by one") for i in range(no)]
		        listip=[item for item in listip if item in sortedip]
			dnlist=listip[:]
        else:
		ddflag=2
	        listip=list()
	        listip=[raw_input("Enter ip one by one") for i in range(no)]
	        listip=[item for item in listip if item in sortedip]
		dnlist=listip[:]
#-------------------------------------------------------------------------------------------------------------			
#For nodemanager
        no=int(raw_input("How many 'nodemanager' you want to have in your cluster ? "))
        if no > len(sortedip) :
	        print "You dont have that much commodity hardwares! Enter value less than {} ".format(len(sortedip))
	        no=int(raw_input("How many 'nodemanager you want to make ? "))
	        if no > len(sortedip) :
			nmflag=1		        
			print "Making all the left over commodity hardwares as 'nodemanager"
			ttlist=sortedip[:]
	        else:
			nmflag=2
	                lisip=list()
		        lisip=[raw_input("Enter ip one by one ") for i in range(no)]
		        lisip=[item for item in listip if item in sortedip]
			nmlist=lisip[:]
        else:
		nmflag=2
	        lisip=list()
                lisip=[raw_input("Enter ip one by one ") for i in range(no)]
	        lisip=[item for item in listip if item in sortedip]
		nmlist=lisip[:]	

system("sshpass -p redhat ssh -l root {} hostnamectl set-hostname nn".format(nip))
system("sshpass -p redhat ssh -l root {} hostnamectl set-hostname rm".format(rip))
count=1
nm=1
dn=1
for i in nmlist:
	if i in dnlist:
		system("echo '{}  dn-nm{} ' >> /di/hosts ".format(i,count))
		system("sshpass -p redhat ssh -l root {} hostnamectl set-hostname dn-nm{}".format(i,count))
		count+=1
		dnlist.remove(i)
	else:
		system("echo '{}  nm{} ' >> /di/hosts ".format(i,nm))
		system("sshpass -p redhat ssh -l root {} hostnamectl set-hostname nm{}".format(i,nm))
		nm+=1
for i in dnlist:
	system("echo '{}  dn{} ' >> /di/hosts ".format(i,dn))
	system("sshpass -p redhat ssh -l root {} hostnamectl set-hostname dn{}".format(i,dn))
	dn+=1
#Starting all the services
#-------------------------------------------------------------------------------------------------------------
def start_services():
	mymodule.start_namenode(nip)
	mymodule.start_resourcemanager(rip)
    	if flag==1:
		if dflag==1:
			mymodule.start_dnnm(sortedip)
		elif dflag==2:
			mymodule.start_dnnm(listip)
	else:
		if ddflag==1:
			mymodule.start_datanodes(sortedip)
		else:
			mymodule.start_datanodes(listip)
		if nmlag==1:
			mymodule.start_nodemanager(sortedip)
		else:
			mymodule.start_nodemanager(lisip)
		
start_services()					
