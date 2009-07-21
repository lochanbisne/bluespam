#!/bin/sh

avahi-publish-service "BlueSpam status" _http._tcp 80 &

cd /opt/spam/branches/mvn/spam/

# ./init_rfcomm.sh

./initialize
./start hci0 -a
