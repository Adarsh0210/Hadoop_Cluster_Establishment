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
		system("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} '{1}; {2}'".format(nip,z1,z2))	
	elif x[1]=='2.6.4' :
		flag=2
	else :
		flag=1
	if flag==1:
		system("sshpass -p redhat scp -r /hadoop2 root@{}:/ ".format(nip))
		system("sshpass -p redhat scp /di/Hadoop2Files/Namenode/core-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(nip))
                system("sshpass -p redhat scp /di/Hadoop2Files/Namenode/hdfs-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(nip))
	else:	
		system("sshpass -p redhat scp /di/Hadoop2Files/Namenode/core-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(nip))
		system("sshpass -p redhat scp /di/Hadoop2Files/Namenode/hdfs-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(nip))

	system("sshpass -p redhat scp -r /di/.bashrc root@{}:/root/ ".format(nip))
	system("sshpass -p redhat scp /root/Desktop/Python/hosts root@{}:/etc/ ".format(nip))
	e1="export JAVA_HOME=/usr/java/jdk1.7.0_79/"
	e2="export HADOOP_HOME=/hadoop2/"
	e3="export PATH=/hadoop2/bin/:/hadoop2/sbin/:$PATH"
	e4="export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH"
	x="rm -rf /name"
	y="mkdir /name"
	z="echo 'Y\n' | hadoop namenode -format "
	a="hadoop-daemon.sh start namenode"	
	system("sshpass -p redhat ssh -l root {0} \"{1}; {2}; {3}; {4}; {5}; {6}; {7}; {8}\"".format(nip,e1,e2,e3,e4,x,y,z,a))        

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
		system("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{0} '{1}; {2}'".format(i,z1,z2))	
		elif x[1]=='2.6.4':
			flag=2		
		else :
			flag=1
		if flag==1:
			system("sshpass -p redhat scp -r /hadoop2 root@{}:/ ".format(i))
			system("sshpass -p redhat scp /di/Hadoop2Files/Datanode/core-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(i))
                        system("sshpass -p redhat scp /di/Hadoop2Files/nodemanager/yarn-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(i))
                        system("sshpass -p redhat scp /di/Hadoop2Files/Datanode/hdfs-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(i))
		else:	
			system("sshpass -p redhat scp /di/Hadoop2Files/Datanode/core-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(i))
			system("sshpass -p redhat scp /di/Hadoop2Files/nodemanager/yarn-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(i))
			system("sshpass -p redhat scp /di/Hadoop2Files/Datanode/hdfs-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(i))
		
		system("sshpass -p redhat scp -r /di/.bashrc root@{}:/root/ ".format(i))
		system("sshpass -p redhat scp /root/Desktop/Python/hosts root@{}:/etc/ ".format(i))
		e1="export JAVA_HOME=/usr/java/jdk1.7.0_79/"
		e2="export HADOOP_HOME=/hadoop2/"
		e3="export PATH=/hadoop2/bin/:/hadoop2/sbin/:$PATH"
		e4="export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH"
		x="rm -rf /data"
		y="mkdir /data"
		a="hadoop-daemon.sh start datanode"	
		b="yarn-daemon.sh start nodemanager"	        
		system("sshpass -p redhat ssh -l root {} setenforce 0".format(i))		
		system("sshpass -p redhat ssh -l root {0} \"{1}; {2}; {3}; {4}; {5}; {6}; {7}; {8};\"".format(e1,e2,e3,e4,x,y,a,b))	
#function for resourcemanager
def start_resourcemanager(rm):
	cmd="hadoop version | grep Hadoop | cut -f2 -d' '"	
	x=getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@{} {}".format(rm,cmd))
	flag=0	
	if x[1]=='1.2.1':
		flag=1		
		system("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@yum remove hadoop -y".format(i))	
	elif x[1]=='2.6.4':
		flag=2		
	else :
		flag=1
	if flag==1:
		system("sshpass -p redhat scp -r /hadoop2 root@{}:/ ".format(rm))
		system("sshpass -p redhat scp /di/Hadoop2Files/resourcemanager/core-site.xml root@{0}:/hadoop2/etc/hadoop/".format(rm))
		system("sshpass -p redhat scp /di/Hadoop2Files/resourcemanager/yarn-site.xml root@{0}:/hadoop2/etc/hadoop/".format(rm))
	else:	
		system("sshpass -p redhat scp /di/Hadoop2Files/resourcemanager/core-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(rm))
		system("sshpass -p redhat scp /di/Hadoop2Files/resourcemanager//yarn-site.xml root@{}:/hadoop2/etc/hadoop/ ".format(rm))

	system("sshpass -p redhat scp -r /di/.bashrc root@{}:/root/ ".format(rm))
	system("sshpass -p redhat scp /di/hosts root@{}:/etc/ ".format(rm))
	e1="export JAVA_HOME=/usr/java/jdk1.7.0_79/"
	e2="export HADOOP_HOME=/hadoop2/"
	e3="export PATH=/hadoop2/bin/:/hadoop2/sbin/:$PATH"
	e4="export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH"
	a="yarn-daemon.sh start resourcemanager"	
	system("sshpass -p redhat ssh -l root {0} \"{1}; {2}; {3}; {4}; {5}\"".format(rm,e1,e2,e3,e4,a))        


