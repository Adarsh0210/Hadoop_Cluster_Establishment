#!/usr/bin/python2

import os,cgi,cgitb
from commands import getstatusoutput
cgitb.enable()

print "content-type:text/html\n"

print """<!DOCTYPE html>
<style>
body{
background-color:white;
/*background-image:url('/var/www/html/bg4.jpg');*/
}
div{
color:black;
text-align:center;
text-shadow:5px 5px 10px grey;
}
}
</style>

<html>

<head>
<title>ViewFiles</title>
</head>
<body>
<div>
"""

form=cgi.FieldStorage()
m=form['mapper']
r=form['reducer']
f=form['fname']
o=form['output']
if m.filename:
	fn1=os.path.basename(m.filename)
	open('../uploads/' + fn1,'wb').write(m.file.read())
	x=getstatusoutput("docker cp /var/www/uploads/{}  client:/".format(fn1))
if r.filename:
	fn2=os.path.basename(r.filename)
	open('../uploads/' + fn2,'wb').write(r.file.read())
	x=getstatusoutput("docker cp /var/www/uploads/{}  client:/".format(fn2))
print f.value
print o.value
x=getstatusoutput("sudo docker exec -i client hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -input {0} -file {1}  -mapper  ./{1} -file {2} -reducer ./{2} -output {3} ".format(f.value,fn1,fn2,o.value))
print x[1]	
print """</div>
</body>

</html>
"""

