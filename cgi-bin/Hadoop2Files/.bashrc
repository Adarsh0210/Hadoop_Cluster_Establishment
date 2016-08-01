# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
export JAVA_HOME=/usr/java/jdk1.7.0_79/
export HADOOP_HOME=/hadoop2/
export PATH=/hadoop2/bin/:/hadoop2/sbin/:$PATH
export PATH=/usr/java/jdk1.7.0_79/bin/:$PATH
