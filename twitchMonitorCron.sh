#!/bin/bash

restartDiscordListener=0
restartStreamNotification=0
while read -r line
do
    len=${#line}
    i=0
    while [ $i -lt $len ]
    do
        substr=${line:i}
        found=`expr match "$substr" discordListener.py`
        if [ $found -gt 0 ]
        then
            restartDiscordListener=0
            break 2
        fi
        i=`expr $i + 1`
    done
    restartDiscordListener=1
done < <(ps -aux | grep discordListener)

while read -r line
do
    len=${#line}
    i=0
    while [ $i -lt $len ]
    do
        substr=${line:i}
        found=`expr match "$substr" streamNotificationBroadcaster.py`
        if [ $found -gt 0 ]
        then
            restartStreamNotification=0
            break 2
        fi
        i=`expr $i + 1`
    done
    restartStreamNotification=1
done < <(ps -aux | grep streamNotificationBroadcaster)

if [ $restartDiscordListener -eq 1 ]
then
    echo "restarting discordListener"
    /usr/bin/python3 /srv/git/StreamNotifcationsBot/discordListener.py &
fi

if [ $restartStreamNotification -eq 1 ]
then
    echo "restarting streamNotificationBroadcaster"
    /usr/bin/python3 /srv/git/StreamNotificationsBot/streamNotificationBroadcaster.py &
fi
