#!/bin/bash

echo "!!! Run me with sudo !!!"
echo "Reminder, modify the scidash_start.sh and scidash_stop.sh scripts"
echo "to point to the right deployment folder and then run me again"
cp scidash_popd.sh /usr/local/bin/
cp scidash_start.sh /usr/local/bin/
cp scidash_stop.sh /usr/local/bin/
cp check_celery_beat.sh /usr/local/bin/
cp scidash_check_service.sh /usr/local/bin/
