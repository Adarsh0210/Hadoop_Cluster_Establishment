#!/usr/bin/python

print "content-type:text/html"
print ""

import cgi,cgitb
cgitb.enable()

import mysql.connector as mariadb

db=mariadb.connect(user='root',password='redhat',database='user')

cursor=db.cursor()

userinput=cgi.FormContent()
#Taking form inputs
username=userinput['username'][0]
email=userinput['email'][0]
password=userinput['password'][0]
rpassword=userinput['rpassword'][0]

if password != rpassword or password=='' or email=='' or username=='':
	print "<META HTTP-EQUIV=refresh CONTENT=\"0,URL=http://192.168.43.4/login.html\">\n"
else:	
	cursor.execute("INSERT into users(name,email,password) VALUES (%s,%s,%s)",(username,email,password))
	print "<META HTTP-EQUIV=refresh CONTENT=\"0,URL=http://192.168.43.4/establish.html\">\n"
db.commit()
db.close()
	

