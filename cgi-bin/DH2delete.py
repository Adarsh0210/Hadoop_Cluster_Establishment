#!/usr/bin/python2

import cgi,cgitb
from commands import getstatusoutput
cgitb.enable()

x=cgi.FormContent()
fname=x['fname'][0]
print "content-type:text/html\n"
z=getstatusoutput("sudo docker exec -i client /hadoop2/bin/hdfs dfs -rm {}".format(fname))
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
print z[1]
print """
</p>
</body>
</html>
"""


