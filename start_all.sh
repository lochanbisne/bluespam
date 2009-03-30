#!/bin/sh

sudo ./init_rfcomm.sh

./initialize

for dev in `hcitool dev | awk '{print $1}' | grep hci`; do

  ./start $dev -a &
done
