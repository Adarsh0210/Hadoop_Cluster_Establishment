#!/usr/bin/python2

from os import system 
from commands import getstatusoutput
import cgi,time

print "content-type:text/html"
print ""

x=cgi.FormContent()
keys=x.keys()
fh=open("/var/www/html/redirect.html","w+")
fh.write("\n<script type='text/javascript'>\nfunction submitForm() {\n")
for i in keys:
	fh.write("var {0} = {0};\n".format(i))
fh.write("var http = new XMLHttpRequest();\n")
fh.write("http.open('GET','http://192.168.43.4/cgi-bin/manual.py?")
count=1
for i in keys:
	if count==1:
        	fh.write("{0}={0}".format(i))
	else:
		fh.write("&{0}={0}".format(i))	
	count+=1

fh.write("',true);\n")
fh.write("http.setRequestHeader('Content-type','application/x-www-form-urlencoded')\n");
fh.write("http.send({});\n".format(i))
        
#fh.write("http.onload = function() {\nalert(http.responseText);\n}\n     }\n")

fh.write("</script>\n")
#fh.write("<form action='http://192.168.43.4/cgi-bin/manual.py'>\n")
fh.write("</br></br><p align=center><input type='button' onclick='submitForm();' value='CLICK HERE TO CONTINUE'>\n</p>")

print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/redirect.html\">\n"

http.open('GET','http://192.168.43.4/cgi-bin/manual.py?a1=' + a1 + '&c3=' + c3 + '&d4=' + d4 + '&e2=' + e2 ,true);
