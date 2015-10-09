#!/bin/sh

SERVICE="$1"
RESULT=`ps -a | sed -n /${SERVICE}/p`

if [ "${RESULT:-null}" = null ]; then
    echo "not running"
    /groups/soundcloudninjas/sound_cloud_analytics/soundcloudninjas/bin/python /groups/soundcloudninjas/sound_cloud_analytics/webscraper/scloudanalytics.py
else
    DONOTHING=1
fi
