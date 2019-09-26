
adb shell mkdir -p /data/lighttpd/www/vhosts
adb shell mkdir -p/data/etc/lighttpd/conf.d
REM adb push ./lighttpd.conf /data
REM adb shell chmod 777 /data/lighttpd.conf

adb shell rm /data/etc/lighttpd -rf

rem step 1. get original file
adb shell mkdir -p /data/etc
adb push etc/lighttpd /data/etc/

rem step 2. modify file
adb push lighttpd.conf /data/etc/lighttpd
adb push dirlisting.conf /data/etc/lighttpd/conf.d
adb push cgi.conf /data/etc/lighttpd/conf.d

rem step 3. push script
REM adb push ./wait_to_record.sh /data
adb push ./start_httpd.sh /data
adb push ./after_app.sh /data
adb push ./audio_record.sh /data


rem step 4. push other data
adb push www /data/lighttpd
adb push cgi-bin /data/lighttpd/www
adb push resources /data/lighttpd

rem step 5. chown
adb shell chown www-data:www-data /data/lighttpd -R
adb shell chown www-data:www-data /data/etc -R
adb shell chmod 777 /data/lighttpd -R
echo "please input machine tag(one for 1m, three for 3m, five for 5m):"
set /p machine_name=
adb push machines/%machine_name%/machine_name  /data/lighttpd

adb shell chmod 777 -R /data/

rem step 6. reboot
adb shell reboot

pause
