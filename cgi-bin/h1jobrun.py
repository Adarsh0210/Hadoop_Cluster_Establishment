#!/usr/bin/python2

import os,cgi,cgitb
from commands import getstatusoutput
cgitb.enable()

print "content-type:text/html\n"

form=cgi.FieldStorage()
m=form['mapper']
r=form['reducer']
f=form['fname']
o=form['output']
if m.filename:
	fn1=os.path.basename(m.filename)
	open('../uploads/' + fn1,'wb').write(m.file.read())
if r.filename:
	fn2=os.path.basename(r.filename)
	open('../uploads/' + fn2,'wb').write(r.file.read())
print f.value
print o.value
x=getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@192.168.43.4 hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -input {0} -file /var/www/uploads/{1}  -mapper  ./var/www/uploads/{1} -file /var/www/uploads/{2} -reducer ./var/www/uploads/{2} -output {3} ".format(f.value,fn1,fn2,o.value))
print x[1]	
