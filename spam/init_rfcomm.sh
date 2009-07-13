#!/bin/sh

# This file needs to be run every time the linux box restarts

for i in 0 1 2 3 4 5 6 7 8 9; do
  mknod /dev/rfcomm$i c 216 $i;
  chmod 0660 /dev/rfcomm$i
  chgrp dialout /dev/rfcomm$i
  rfcomm release /dev/rfcomm$i
done


