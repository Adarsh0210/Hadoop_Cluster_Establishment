#!/usr/bin/python2

from os import system 
from commands import getstatusoutput
import mymodule
import thread
import cgi

print "content-type:text/html"
print "\n"
def collect_ip(start,end):
#using nmap to collect the list of ips
	x=getstatusoutput("nmap -sP {}-{} -n | grep 'Nmap scan'| cut -f5 -d' ' > /var/www/cgi-bin/nmap1.txt".format(start,end[3]))
	fhandle=open("/var/www/cgi-bin/nmap1.txt","rw+")
	fwrite=open("/var/www/html/form.html","w+")
	fh=open("/var/www/cgi-bin/nmap2.txt","w+")
	fwrite.write("<style>\ntable#id1\n{\nbackground-color: teal;\ncolor: yellow;\nborder-radius: 10px;\nborder: 5px solid silver;\nborder-style: groove;\n}\ninput.class2\n{\nposition: absolute;\nleft: 38%;\n}\nh1.class1\n{\ncolor: aqua;\ntext-shadow: 2px 2px 2px white;\n}\n</style>\n<body background='b2.jpg' >\n<h1 class='class1' align='center'><b><i>STASTISTICS OF THE NODES IN THE NETWORK</i></b></h1>")
	fwrite.write("<form action='http://192.168.43.4/cgi-bin/Hadoop2/manual.py' name=\"formname\">\n<table id='id1' rules='all'>\n<tr>\n<td width=9.1%>I.P.</td>\n<td width=9.1%>RAM</td>\n<td width=9.1%>CPU</td>\n<td width=9.1%>HARD DISK</td>\n<td width=9.1%>N.N.</td>\n<td width=9.1%>R.M.</td>\n<td width=9.1%>D.N.</td>\n<td width=9.1%>N.M.</td>\n<td width=9.1%>D.N. & N.M.</td>\n</tr>\n")	
	lis=list()
	for lines in fhandle:
		lis.append(lines)
	excludeip=['192.168.43.110','192.168.43.4','192.168.43.2','192.168.43.53','192.168.43.1','192.168.43.12']
	count=0
#	print lis
#	raw_input()	
	for items in lis:
		items=items.strip()
		if items not in excludeip:
			fh.write(items)
			fh.write('\n')			
			count+=1			
			x1="cat /proc/meminfo | grep 'MemTotal:' | cut -f9 -d' ' "
			x2=" lscpu | grep 'CPU MHz:' | cut -f17 -d' '"
			x3=" df -hT | grep '/dev/mapper/rhel-root' | cut -f3 -d'G'" 
			x4="sshpass -p redhat ssh -o StrictHostKeyChecking=no -l root {0} \" {1}; {2}; {3}\"".format(items,x1,x2,x3)
			x=getstatusoutput(x4)
			z=x[1].split('\n')
			fwrite.write("<tr>\n<td width=10%>{0}</td>\n<td width=10%>{1}</td>\n<td width=10%>{2}</td>\n<td width=10%>{3}</td>\n".format(items,z[0],z[1],z[2]))
			x="document.formname.b{0}.checked=false; document.formname.c{0}.checked=false; document.formname.d{0}.checked=false; document.formname.e{0}.checked=false; ".format(count)
			y="<td width=9.1%><input type=\"checkbox\" name='a{0}' id='a{0}'".format(count)
			fwrite.write( y + " onclick=\"if(this.checked) {" + x)
			i=1
			for i in range(1,len(lis)+1):
				if i!=count:
					fwrite.write(" document.formname.a{0}.checked=false;".format(i))
			fwrite.write("}\" /></td>\n")

			x="document.formname.a{0}.checked=false; document.formname.c{0}.checked=false; document.formname.d{0}.checked=false; document.formname.e{0}.checked=false; ".format(count)
			y="<td width=9.1%><input type=\"checkbox\" name='b{0}' id='b{0}'".format(count)
			fwrite.write( y + " onclick=\"if(this.checked) {" + x)			
			i=1
			for i in range(1,len(lis)+1):
				if i!=count:
					fwrite.write(" document.formname.b{0}.checked=false;".format(i))
			fwrite.write("}\" /></td>\n")

			x="document.formname.b{0}.checked=false; document.formname.d{0}.checked=false; document.formname.a{0}.checked=false; document.formname.e{0}.checked=false; ".format(count)
			y="<td width=9.1%><input type=\"checkbox\" name='c{0}' id='c{0}'".format(count)
			fwrite.write( y + " onclick=\"if(this.checked) {" + x + "}\" /></td>\n")
			
			

			y="<td width=9.1%><input type=\"checkbox\" name='d{0}' id='d{0}'".format(count)
			x="document.formname.b{0}.checked=false; document.formname.c{0}.checked=false; document.formname.e{0}.checked=false; document.formname.a{0}.checked=false; ".format(count)
			fwrite.write( y + " onclick=\"if(this.checked) {" + x + "}\" /></td>\n")

			x="document.formname.b{0}.checked=false; document.formname.c{0}.checked=false; document.formname.d{0}.checked=false; document.formname.a{0}.checked=false; ".format(count)			
			y="<td width=9.1%><input type=\"checkbox\" name='e{0}' id='e{0}'".format(count)
			fwrite.write( y + " onclick=\"if(this.checked) {" + x + "}\" /></td>\n")

	fwrite.write("</table>\n<br />\n<input class='class2' type=\"submit\" value=\"click here to establish your cluster...\"/>\n</form>\n</body>")
	fhandle.close()
	fwrite.close()


x=cgi.FormContent()
start=x['START'][0]
end=x['END'][0]
#start="192.168.43.10"
#end="192.168.43.20"
end=end.strip().split('.')
collect_ip(start.strip(),end)

print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.4/form.html\">\n"



