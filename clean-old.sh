#!/bin/bash

CAMDIR=/var/www/html/cams

find $CAMDIR -name "*.jpg" -ctime +4 -exec rm {} \;
find $CAMDIR -name "*.mp4" -ctime +4 -exec rm {} \;
