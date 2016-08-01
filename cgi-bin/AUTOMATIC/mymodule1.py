#!/usr/bin/python2
from os import system
from commands import getstatusoutput
import thread

#function to update block size 
"""def update_blocksize():
	print "What is the default block size you want to have!\n"	
	try:	
		size=raw_input("Enter the block size in MB's eg. 64 or 128 ....\n")
		size=int(size)*1024*1024
	except:
		print "Invalid entry! Only enter integers"
		size=1	
	while size % 512 != 0:
		print "Invalid block size!Block size should be in multiple of 512"
		size=raw_input("Enter the block size in MB's eg. 64 or 128 ....\n")
		size=int(size)*1024*1024
	fh=open("/root/Desktop/Python/ConfigurationFiles/Datanode/hdfs-site.xml",'rw+')
	for line in fh:
		if '</configuration>' in line:
			break
	fh.seek(fh.tell()-len('</configuration>\n')-1,0)
	fh.write("\n<property>\n<name>dfs.block.size</name>\n<value>{}</value>\n</property>\n\n</configuration>\n".format(size))
	fh.close()

#Function to update replication factor
def update_replicationfactor():
	print "What is the default replication factor you want to have!\n"	
	while True:	
		try:	
			no=raw_input("Enter the numbers eg. 2 or 3 ....\n")
			no=int(no)
			break
		except:
			print "Invalid entry! Only enter integers\nEnter again!\n"
			
	fh=open("/root/Desktop/Python/ConfigurationFiles/Datanode/hdfs-site.xml",'rw+')
	for line in fh:
		if '</configuration>' in line:
			break
	fh.seek(fh.tell()-len('</configuration>\n')-1,0)
	fh.write("\n<property>\n<name>dfs.replication</name>\n<value>{}</value>\n</property>\n\n</configuration>\n".format(no))
	fh.close()

#function to set checkpointing duration
def update_checkpointing():	
	print "What is the checkpointing duration you want to set!The default is 3600 seconds\n"	
	while True:	
		try:	
			no=raw_input("Enter the time in seconds....\n")
			no=int(no)
			break
		except:
			print "Invalid entry! Only enter integers\nEnter again!\n"
			
	fh=open("/root/Desktop/Python/ConfigurationFiles/SNN/hdfs-site.xml",'rw+')
	for line in fh:
		if '</configuration>' in line:
			break
	fh.seek(fh.tell()-len('</configuration>\n')-1,0)
	fh.write("\n<property>\n<name>fs.checkpoint.period</name>\n<value>{}</value>\n</property>\n\n</configuration>\n".format(no))
	fh.close()
"""

#function for namenode
def start_namenode(nip):
        system("sshpass -p redhat ssh -l root {} setenforce 0".format(nip))
	system("sshpass -p redhat scp /root/Desktop/Python/hosts  root@{}:/etc/ ".format(nip))
	system("sshpass -p redhat scp /root/Desktop/Python/ConfigurationFiles/Namenode/hdfs-site.xml root@{}:/etc/hadoop/hdfs-site.xml".format(nip))	
	system("sshpass -p redhat scp /root/Desktop/Python/ConfigurationFiles/Namenode/core-site.xml root@{}:/etc/hadoop/core-site.xml".format(nip))	
	system("sshpass -p redhat ssh -l root {} rm -rf /name".format(nip))        
	system("sshpass -p redhat ssh -l root {} mkdir /name".format(nip))            
	system("sshpass -p redhat ssh -l root {} echo 'Y\n' | hadoop namenode -format ".format(nip))
	system("sshpass -p redhat ssh -l root {} hadoop-daemon.sh start namenode".format(nip))

#function for datanodes
numthreads=0
threadstarted=False
lock=thread.allocate_lock()
def start_dn(i):
	global numthreads,threadstarted
	lock.acquire()
	numthreads+=1
	threadstarted=True
	lock.release()
        system("sshpass -p redhat ssh -l root {} setenforce 0".format(i))		
	system("sshpass -p redhat scp /root/Desktop/Python/hosts   root@{}:/etc/ ".format(i))
	system("sshpass -p redhat ssh -l root {} rm -rf /data".format(i))        
       	system("sshpass -p redhat ssh -l root {} mkdir /data".format(i))    
	system("sshpass -p redhat scp /root/Desktop/Python/ConfigurationFiles/Datanode/hdfs-site.xml root@{}:/etc/hadoop/hdfs-site.xml".format(i))	
	system("sshpass -p redhat scp /root/Desktop/Python/ConfigurationFiles/Datanode/core-site.xml root@{}:/etc/hadoop/core-site.xml".format(i))
	system("sshpass -p redhat ssh -l root {} hadoop-daemon.sh start datanode ".format(i))
	lock.acquire()
	numthreads-=1
	lock.release()

def start_datanodes(listip):
#	update_blocksize()
#	update_replicationfactor()
	global numthreads,threadstarted
	for i in listip:
	        thread.start_new_thread(start_dn,(i,))
	while not threadstarted :
		pass
	while numthreads > 0 :
		pass

#function for tasktrackers
num_thread=0
thread_start=False
loc=thread.allocate_lock()
def start_tt(i):
	global num_thread,thread_start
	loc.acquire()
	num_thread+=1
	thread_start=True
	loc.release()
	system("sshpass -p redhat ssh -l root {} setenforce 0; iptables -F".format(i))
	system("sshpass -p redhat scp /root/Desktop/Python/hosts root@{}:/etc/ ".format(i))
	system("sshpass -p redhat scp /root/Desktop/Python/ConfigurationFiles/JT_TT/mapred-site.xml  root@{}:/etc/hadoop/mapred-site.xml".format(i))	
	system("sshpass -p redhat ssh -l root {} hadoop-daemon.sh start tasktracker ".format(i))
	loc.acquire()
	num_thread-=1
	loc.release()

def start_tasktrackers(listip):
	global num_thread,thread_start
	for j in listip:
	        thread.start_new_thread(start_tt,(j,))
	while not thread_start :
		pass	
	while num_thread > 0 :
		pass

#function for jobtracker
def start_jobtracker(jip):
	system("sshpass -p redhat scp /root/Desktop/Python/hosts root@{}:/etc/ ".format(jip))
	system("sshpass -p redhat scp /root/Desktop/Python/ConfigurationFiles/JT_TT/mapred-site.xml root@{}:/etc/hadoop/".format(jip))
        system("sshpass -p redhat scp /root/Desktop/Python/ConfigurationFiles/JT_TT/core-site.xml root@{}:/etc/hadoop/".format(jip))
        system("sshpass -p redhat ssh -l root {} setenforce 0".format(jip))
        x=getstatusoutput("sshpass -p redhat ssh -l root {} /usr/java/jdk1.7.0_79/bin/jps".format(jip))
        system("sshpass -p redhat ssh -l root {} hadoop-daemon.sh start jobtracker".format(jip))

#function for secondary namenode
def start_secondarynamenode(sip):
#	update_checkpointing()	
	system("sshpass -p redhat ssh -l root {} setenforce 0".format(sip))
	system("sshpass -p redhat scp /root/Desktop/Python/hosts root@{}:/etc/ ".format(sip))
	system("sshpass -p redhat ssh -l root {} rm -rf /data ".format(sip))	
	system("sshpass -p redhat ssh -l root {} 'mkdir -p /data/edits /data/current'".format(sip))
	x=getstatusoutput("sshpass -p redhat ssh -l root {} /usr/java/jdk1.7.0_79/bin/jps ".format(sip))
	system("sshpass -p redhat scp /root/Desktop/Python/ConfigurationFiles/SNN/core-site.xml  root@{}:/etc/hadoop/core-site.xml".format(sip))
	system("sshpass -p redhat scp /root/Desktop/Python/ConfigurationFiles/SNN/hdfs-site.xml  root@{}:/etc/hadoop/hdfs-site.xml".format(sip))
	system("sshpass -p redhat ssh -l root {} hadoop-daemon.sh start secondarynamenode ".format(sip))
						
	
