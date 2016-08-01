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
	x=getstatusoutput("docker cp /var/www/uploads/{}  client:/".format(fn))
	print x[1]
	y=getstatusoutput("docker exec -i client hadoop fs -put /{} /".format(fn))		
	print y[1]	
	message='The file ' + fn + ' was successfully uploaded'
else:
	message='The file ' + fn + ' was not uploaded'

print """<p>%s</p>
</body>
</html>
"""%(message,)
