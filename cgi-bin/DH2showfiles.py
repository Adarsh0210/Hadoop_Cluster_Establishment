#!/usr/bin/python2

from commands import getstatusoutput
import cgi,cgitb

cgitb.enable()

print "content-type:text/html"
print ""
x=cgi.FormContent()
y=x['dname'][0]
z=getstatusoutput("sudo docker exec -i client /hadoop2/bin/hdfs dfs -ls {0}".format(y))
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
print "<p>"
x=z[1].split('\n')
for lines in x:
	print lines
print "</p>"
print """</div>
</body>

</html>
"""

