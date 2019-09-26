echo "Content-type:text/html"
echo ""

id=""
age=""
gender=""
province=""
time=""
LINE=`echo $QUERY_STRING | sed 's/&/ /g'`
for LOOP in $LINE
do
    NAME=`echo $LOOP | sed 's/=/ /g' | awk '{print $1}'`
    TYPE=`echo $LOOP | sed 's/=/ /g' | awk '{print $2}' | sed -e 's/%\(\)/\\\x/g' | sed 's/+/ /g'`
    if [ "$NAME" == "id" ]; then
        id=$TYPE
    fi
    if [ "$NAME" == "age" ]; then
        age=$TYPE
    fi
    if [ "$NAME" == "gender" ]; then
        gender=$TYPE
    fi
    if [ "$NAME" == "province" ]; then
        province=$TYPE
    fi
    if [ "$NAME" == "time" ]; then
        time=$TYPE
    fi
done


target=/data/lighttpd/www/cgi-bin
echo -n $id > $target/id
echo -n $age > $target/age
echo -n $gender > $target/gender
echo -n $province > $target/province
echo -n $time > $target/time
