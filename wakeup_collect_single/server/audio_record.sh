#!/bin/sh

cvlc -q --no-interact --play-and-exit /data/lighttpd/resources/du.mp3
machine_name=`cat /data/lighttpd/machine_name`

id=`cat /data/lighttpd/www/cgi-bin/id`
age=`cat /data/lighttpd/www/cgi-bin/age`
gender=`cat /data/lighttpd/www/cgi-bin/gender`
province=`cat /data/lighttpd/www/cgi-bin/province`
time=`cat /data/lighttpd/www/cgi-bin/time`
if [ "$machine_name" == "one" ] ;then
	prefix="D1"
fi
if [ "$machine_name" == "three" ] ;then
	prefix="D3"
fi
if [ "$machine_name" == "five" ] ;then
	prefix="D5"
fi

if [ ! -d /data/lighttpd/www/cgi-bin/output ]; then
	mkdir -p /data/lighttpd/www/cgi-bin/output
	chmod 777 -R /data/lighttpd/www/cgi-bin/output
fi




#echo $filename
arecord  -t raw -f S16_LE -c 8 -r 16000  /data/lighttpd/www/cgi-bin/output/$id.pcm
chmod 777 -R /data/lighttpd/www/cgi-bin/output/

