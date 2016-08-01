#!/usr/bin/python2

print "content-type:text/html"
print "\n"

from os import system 
import getpass
from commands import getstatusoutput
import mymodule
import thread
import cgi


system("echo '127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1          localhost localhost.localdomain localhost6 localhost6.localdomain6\n' > /var/www/cgi-bin/hosts ")

#x=cgi.FormContent()
#keys=x.keys()


ip=list()
fh=open("/var/www/cgi-bin/nmap2.txt","rw+")
for ips in fh:
	i=ips.strip()
	ip.append(i)
fh.close()

nip=0
sip=0
jip=0
hip=0
dnip=list()
ttip=list()
dnttip=list()
keys=['a1','b2','c3','d4','g5']
for items in keys:
	print items
	raw_input()
	if items[0]=='a':
		nip=ip[int(items[1:])-1]
	elif items[0]=='b':
		sip=ip[int(items[1:])-1]
	elif items[0]=='c':
		jip=ip[int(items[1:])-1]
	elif items[0]=='d':
		l=int(items[1:])
		k=ip[l-1]
		print k
		dnip.append(k)
	elif items[0]=='e':
		l=int(items[1:])
		k=ip[l-1]
		print k
		ttip.append(k)
	elif items[0]=='f':
		l=int(items[1:])
		k=ip[l-1]
		print k
		dnttip.append(k)
	elif items[0]=='g':
		hip=ip[int(items[1:])-1]
"""

nip="192.168.43.3"
hip="192.168.43.4"
jip="192.168.43.11"
sip="192.168.43.12"
dnip=list()
ttip=list()
dnttip=["192.168.43.111"]

"""
print nip
print jip
print sip
print dnttip
print dnip
print ttip
print hip

