adb push www /data/lighttpd

adb push cgi-bin /data/lighttpd/www
adb shell chmod 777 -R /data/lighttpd/www
adb shell chown www-data:www-data -R /data/lighttpd/www

adb push resources /data/lighttpd


adb push audio_record.sh /data
adb push start_httpd.sh /data

adb push wait_to_stop_record.sh /data

adb shell chmod 777 -R /data/


