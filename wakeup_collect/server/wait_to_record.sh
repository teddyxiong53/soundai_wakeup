#!/bin/sh

while [ "1" == "1" ]; do
    while [ ! -f /data/lighttpd/www/cgi-bin/begin_record ] ; do
        #echo "waiting for record" >> /data/1.log
        sleep 0.2
    done
    echo "begin to record" >> /data/1.log
    /data/audio_record.sh
    rm -rf /data/lighttpd/www/cgi-bin/begin_record
done

