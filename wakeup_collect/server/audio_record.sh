#!/bin/sh

cvlc -q --no-interact --play-and-exit /data/lighttpd/resources/begin_record.mp3
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

for i in $(seq 1 15) ; do
	if [ ! -f /data/lighttpd/www/cgi-bin/begin_record ]; then
		cvlc -q --no-interact --play-and-exit /data/lighttpd/resources/stop_record.mp3
		# this means stop the recording manually
		exit 0
	fi
	cvlc -q --no-interact --play-and-exit /data/lighttpd/resources/du.mp3
	if [ $i -lt 10 ]; then
		filename=$prefix"_"$id"_"$gender"_"$age"_"$province"_000"$i
	else
		filename=$prefix"_"$id"_"$gender"_"$age"_"$province"_00"$i
	fi
	#echo $filename
	arecord  -t wav -f S16_LE -c 4 -r 16000 -d $time /data/lighttpd/www/cgi-bin/output/$filename.wav
done

cvlc -q --no-interact --play-and-exit /data/lighttpd/resources/end_record.mp3
