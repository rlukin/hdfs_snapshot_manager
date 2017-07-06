#!/bin/bash

for (( i=0; i < $1; i++ ))
do
month=$(( ( RANDOM % 7 )  + 1 ))
day=$(( ( RANDOM % 28 )  + 1 ))
date=$(date -d 2017-$a-$b +"%Y%m%d")
echo "/user/developer1/.snapshot/s$date-165612.432"
done
