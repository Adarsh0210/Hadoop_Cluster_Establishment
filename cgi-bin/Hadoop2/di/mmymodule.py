#!/usr/bin/python2
from os import system
from commands import getstatusoutput

#function for namenode
def start_namenode(nip):
	cmd="hadoop version | grep Hadoop | cut -f2 -d' '"	
	x=getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} {1}".format(nip,cmd))
	flag=0	
	if x[1]=='1.2.1':
		flag=1	
		z1="yum remove hadoop -y"
		z2="rm -rf /etc/hadoop"
		getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} '{1}; {2}'".format(nip,z1,z2))	
	elif x[1]=='2.6.4' :
		flag=2
	else :
		flag=1
	if flag==1:
		getstatusoutput("sshpass -p redhat scp -r /var/www/cgi-bin/Hadoop2/Namenode/hadoop2 root@{}:/ ".format(nip))
	else:	
		getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop2/di/Hadoop2Files/Namenode/core-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(nip))
		getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop2/di/Hadoop2Files/Namenode/hdfs-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(nip))

	getstatusoutput("sshpass -p redhat scp -r /var/www/cgi-bin/Hadoop2/di/.bashrc root@{}:/root/ ".format(nip))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/hosts root@{}:/etc/ ".format(nip))
	e1="export JAVA_HOME=/usr/java/jdk1.7.0_79/"
	e2="export HADOOP_HOME=/hadoop2/"
	e3="export PATH=/hadoop2/bin/:/hadoop2/sbin/:$PATH"
	e4="export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH"
	x="rm -rf /name"
	z="hadoop namenode -format "
	a="hadoop-daemon.sh start namenode"	
	getstatusoutput("sshpass -p redhat ssh -l root {0} \"{1}; {2}; {3}; {4}; {5};\"".format(nip,e1,e2,e3,e4,x))        
	getstatusoutput("sshpass -p redhat ssh -l root {0} \"{1}; {2};\"".format(nip,z,a))

#function for datanodes nodemanager
def start_dnnm(listip):
	for i in listip:		
		cmd="hadoop version | grep Hadoop | cut -f2 -d' '"	
		x=getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} {}".format(i,cmd))
		flag=0	
		if x[1]=='1.2.1':
			flag=1	
			z1="yum remove hadoop -y"
			z2="rm -rf /etc/hadoop"
			getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} '{1}; {2}'".format(i,z1,z2))	
		elif x[1]=='2.6.4':
			flag=2		
		else :
			flag=1
		if flag==1:
			getstatusoutput("sshpass -p redhat scp -r /var/www/cgi-bin/Hadoop2/dnnm/hadoop2/ root@{}:/ ".format(i))
		else:	
			getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop2/di/Hadoop2Files/Datanode/core-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(i))
			getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop2/di/Hadoop2Files/nodemanager/yarn-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(i))
			getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop2/di/Hadoop2Files/Datanode/hdfs-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(i))
		
		getstatusoutput("sshpass -p redhat scp -r /var/www/cgi-bin/Hadoop2/di/.bashrc root@{}:/root/ ".format(i))
		getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/hosts root@{}:/etc/ ".format(i))
		e1="export JAVA_HOME=/usr/java/jdk1.7.0_79/"
		e2="export HADOOP_HOME=/hadoop2/"
		e3="export PATH=/hadoop2/bin/:/hadoop2/sbin/:$PATH"
		e4="export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH"
		x="rm -rf /data"
		y="mkdir /data"
		a="hadoop-daemon.sh start datanode"	
		b="yarn-daemon.sh start nodemanager"	        
		getstatusoutput("sshpass -p redhat ssh -l root {0} \"{1}; {2}; {3}; {4}; {5}; {6};\"".format(i,e1,e2,e3,e4,x,y))
		getstatusoutput("sshpass -p redhat ssh -l root {0} \"{1}; {2};\"".format(i,a,b))	
#function for resourcemanager
def start_resourcemanager(rm):
	cmd="hadoop version | grep Hadoop | cut -f2 -d' '"	
	x=getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} {}".format(rm,cmd))
	flag=0	
	if x[1]=='1.2.1':
		flag=1		
		getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@yum remove hadoop -y".format(i))	
	elif x[1]=='2.6.4':
		flag=2		
	else :
		flag=1
	if flag==1:
		getstatusoutput("sshpass -p redhat scp -r /var/www/cgi-bin/Hadoop2/resourcemanager/hadoop2 root@{}:/ ".format(rm))
	else:	
		getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop2/di/Hadoop2Files/resourcemanager/core-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(rm))
		getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/Hadoop2/di/Hadoop2Files/resourcemanager/yarn-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(rm))

	getstatusoutput("sshpass -p redhat scp -r /var/www/cgi-bin/Hadoop2/di/.bashrc root@{}:/root/ ".format(rm))
	getstatusoutput("sshpass -p redhat scp /var/www/cgi-bin/hosts root@{}:/etc/ ".format(rm))
	e1="export JAVA_HOME=/usr/java/jdk1.7.0_79/"
	e2="export HADOOP_HOME=/hadoop2/"
	e3="export PATH=/hadoop2/bin/:/hadoop2/sbin/:$PATH"
	e4="export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH"
	a="yarn-daemon.sh start resourcemanager"	
	getstatusoutput("sshpass -p redhat ssh -l root {0} \"{1}; {2}; {3}; {4};\"".format(rm,e1,e2,e3,e4))
	getstatusoutput("sshpass -p redhat ssh -l root {0} \"{1};\"".format(rm,a))        


