#!/usr/bin/python2

import cgi,cgitb
import os
from commands import getstatusoutput
cgitb.enable()

form=cgi.FieldStorage()

fileitem=form['filename']
print """content-type:text/html\n
<style>
body{
background-color:white;
color:green;
}
</style>
<html>
<body>
"""
if fileitem.filename:
	fn=os.path.basename(fileitem.filename)
	open('../uploads/' + fn,'wb').write(fileitem.file.read())
	y=getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@192.168.43.4 /hadoop2/bin/hdfs dfs -put /var/www/uploads/{} /".format(fn))		
	print y[1]	
	message='The file ' + fn + ' was successfully uploaded'
else:
	message='The file ' + fn + ' was not uploaded'

print """<p>%s</p>
</body>
</html>
"""%(message,)
