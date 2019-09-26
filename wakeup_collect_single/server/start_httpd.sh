#!/bin/sh

# stop app first
/oem/sayinfoos.sh stop

# if [ ! -f /data/dirlisting.conf ]; then
#         cp /etc/lighttpd/conf.d/dirlisting.conf       /data/dirlisting.conf
# fi
# mount --bind  /data/dirlisting.conf  /etc/lighttpd/conf.d/dirlisting.conf

# if [ ! -f /data/lighttpd.conf ]; then
#         cp /etc/lighttpd/lighttpd.conf       /data/lighttpd.conf
# fi
# mount --bind  /data/lighttpd.conf  /etc/lighttpd/lighttpd.conf

mount --bind  /data/etc/lighttpd/  /etc/lighttpd/


# start httpd

/etc/init.d/S50lighttpd restart




