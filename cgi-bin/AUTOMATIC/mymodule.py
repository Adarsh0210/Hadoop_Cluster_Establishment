#!/usr/bin/python2
from os import system
from commands import getstatusoutput
import thread

#print 'content-type:text/html '
#print ""

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
			
	fh=open("/var/www/cgi-bin/Hadoop1Files/SNN/hdfs-site.xml",'rw+')
	for line in fh:
		if '</configuration>' in line:
			break
	fh.seek(fh.tell()-len('</configuration>\n')-1,0)
	fh.write("\n<property>\n<name>fs.checkpoint.period</name>\n<value>{}</value>\n</property>\n\n</configuration>\n".format(no))
	fh.close()


#function for namenode
def start_namenode(nip,hip):
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/hosts  root@{}:/etc/ ".format(nip))
        getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/hosts  root@{}:/etc/ ".format(hip))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/Namenode/hdfs-site.xml root@{}:/etc/hadoop/hdfs-site.xml".format(nip))	
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/Namenode/core-site.xml root@{}:/etc/hadoop/core-site.xml".format(nip))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/HA/hdfs-site.xml root@{}:/etc/hadoop/hdfs-site.xml".format(hip))	
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/HA/core-site.xml root@{}:/etc/hadoop/core-site.xml".format(hip))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/exports root@{}:/etc/ ".format(nip))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/exports root@{}:/etc/ ".format(hip))	
		
	x="rm -rf /name"
	y="mkdir /name"
	u="rm -rf /backup"
	v="mkdir /backup"
	z="echo 'Y\nY\n' | hadoop namenode -format "
	a="hadoop-daemon.sh start namenode"	
	c="systemctl restart nfs-server"		
	i="ifconfig enp0s8:0 192.100.64.2"
	j="ifconfig enp0s8:0 192.100.64.3"
	getstatusoutput("sshpass -p redhat ssh root@{0} \"{1}; {2}; {3}; {4}; {5}\"".format(nip,x,y,u,v,c))
	getstatusoutput("echo '/name    {}(rw,no_root_squash)'> /var/www/cgi-bin/Hadoop1Files/HA/exports".format(nip))
	fh=open("/var/www/cgi-bin/Hadoop1Files/HA/ha.py","rw+")
	for line in fh:
        	if line.startswith('ha'):
                	fh.seek(fh.tell()-len(line),0)
                	fh.write("ha('192.100.64.2','{}')          ".format(nip))
	                break
	fh.close()	
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/HA/exports root@{}:/etc/".format(hip))		
	getstatusoutput("sshpass -p redhat ssh -l root {0} \"{1}; {2}; {3}; {4}\"".format(hip,x,y,c,j))	
	getstatusoutput("sshpass -p redhat ssh -l root {0} 'mount {1}:/name /backup'".format(nip,hip))	
	getstatusoutput("sshpass -p redhat ssh -l root {0} \"{1}; {2};\"".format(nip,i,z))
	#supossing the ha node has nfs-utils installed	
	getstatusoutput("sshpass -p redhat ssh -l root {0} {1}".format(nip,a))		
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/HA/ha.py root@{}:/ ".format(hip))
	getstatusoutput("sshpass -p redhat ssh -l root {0} 'python /ha.py > ~/program.log 2>&1 &' ".format(hip))	
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
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/hosts   root@{}:/etc/ ".format(i))
	getstatusoutput("sshpass -p redhat ssh -l root {} rm -rf /data".format(i))        
       	getstatusoutput("sshpass -p redhat ssh -l root {} mkdir /data".format(i))    
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/Datanode/hdfs-site.xml root@{}:/etc/hadoop/hdfs-site.xml".format(i))	
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/Datanode/core-site.xml root@{}:/etc/hadoop/core-site.xml".format(i))
	getstatusoutput("sshpass -p redhat ssh -l root {} hadoop-daemon.sh start datanode ".format(i))
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
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/hosts root@{}:/etc/ ".format(i))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/JT_TT/mapred-site.xml  root@{}:/etc/hadoop/mapred-site.xml".format(i))	
	getstatusoutput("sshpass -p redhat ssh -l root {} hadoop-daemon.sh start tasktracker ".format(i))
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
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/hosts root@{}:/etc/ ".format(jip))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/JT_TT/mapred-site.xml root@{}:/etc/hadoop/".format(jip))
        getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/JT_TT/core-site.xml root@{}:/etc/hadoop/".format(jip))
        x=getstatusoutput("sshpass -p redhat ssh -l root {} /usr/java/jdk1.7.0_79/bin/jps".format(jip))
        getstatusoutput("sshpass -p redhat ssh -l root {} hadoop-daemon.sh start jobtracker".format(jip))

#function for secondary namenode
def start_secondarynamenode(sip):
#	update_checkpointing()	
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/hosts root@{}:/etc/ ".format(sip))
	getstatusoutput("sshpass -p redhat ssh -l root {} rm -rf /data ".format(sip))	
	getstatusoutput("sshpass -p redhat ssh -l root {} 'mkdir -p /data/edits /data/current'".format(sip))
	x=getstatusoutput("sshpass -p redhat ssh -l root {} /usr/java/jdk1.7.0_79/bin/jps ".format(sip))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/SNN/core-site.xml  root@{}:/etc/hadoop/core-site.xml".format(sip))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop1Files/SNN/hdfs-site.xml  root@{}:/etc/hadoop/hdfs-site.xml".format(sip))
	getstatusoutput("sshpass -p redhat ssh -l root {} hadoop-daemon.sh start secondarynamenode ".format(sip))
						
	
