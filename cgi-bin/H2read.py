#!/usr/bin/python2

import cgi,cgitb
from commands import getstatusoutput
cgitb.enable()

x=cgi.FormContent()
fname=x['fname'][0]
print "content-type:text/html\n"
z=getstatusoutput("sshpass -p redhat ssh -o StrictHostKeyChecking=no root@192.168.43.4 /hadoop2/bin/hdfs dfs -cat {}".format(fname))
print """
<style>
body{
background-color:white;
font-size:15px;
color:black;
text-shadow:4px 4px 5px green;
}

</style>
<html>
<body>
<p>
"""
x=z[1].strip().split('\\n')
for lines in x:
	print lines
print """
</p>
</body>
</html>
"""


