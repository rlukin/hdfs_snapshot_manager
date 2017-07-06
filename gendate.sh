#!/bin/bash

date="20160101"
until [[ $date > "2017-07-06" ]]; do 
    echo "/user/developer1/.snapshot/s$date-165612.432"
    date=$(date -d "$date + 1 day" +"%Y%m%d")
done
