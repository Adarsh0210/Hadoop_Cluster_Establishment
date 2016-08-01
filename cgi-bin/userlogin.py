#!/usr/bin/python2

import cgi,cgitb
from commands import getstatusoutput

print "content-type:text/html"
print ""

cgitb.enable()

import mysql.connector as mariadb

db=mariadb.connect(user='root',password='redhat',database='user')

cursor=db.cursor()

userinput=cgi.FormContent()
username=userinput['username'][0]
userpassd=userinput['password'][0]

cursor.execute("SELECT name from users")
flag=0
for us in cursor:
	if us[0]==username:
		flag=1

if flag==1:
	cursor.execute("SELECT password from users WHERE name=%s",(username,))
	for passwd in cursor:
		password=passwd
	if password[0] == userpassd :
		print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/establish.html\">\n"
	else:
		print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/login.html\">\n"
else:
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/login.html\">\n"
cursor.close()
db.close()



