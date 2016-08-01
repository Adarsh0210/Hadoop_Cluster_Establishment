#function to update block size 
def update_blocksize():
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
	fh=open("/root/Desktop/Hadoop2/dnnn/etc/hadoop/hdfs-site.xml",'rw+')
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
			
	fh=open("/root/Desktop/Hadoop2/dnnn/etc/hadoop/hdfs-site.xml",'rw+')
	for line in fh:
		if '</configuration>' in line:
			break
	fh.seek(fh.tell()-len('</configuration>\n')-1,0)
	fh.write("\n<property>\n<name>dfs.replication</name>\n<value>{}</value>\n</property>\n\n</configuration>\n".format(no))
	fh.close()


