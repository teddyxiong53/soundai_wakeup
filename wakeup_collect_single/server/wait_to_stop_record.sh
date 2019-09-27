#!/bin/sh

while [ "1" == "1" ]; do
    while [ ! -f /data/lighttpd/www/cgi-bin/stop_record ] ; do
        #echo "waiting for record" >> /data/1.log
        sleep 0.2
    done

    killall -9 arecord
    rm -rf /data/lighttpd/www/cgi-bin/stop_record
done

