#!/bin/sh

avahi-publish-service "BlueSpam status" _http._tcp 80 &

cd /opt/spam/tags/1.0/spam/

./init_rfcomm.sh

./initialize
./start hci0 -a
