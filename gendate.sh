#!/bin/bash

for (( i; i < $1; i++ ))
do
a=$(( ( RANDOM % 7 )  + 1 ))
b=$(( ( RANDOM % 20 )  + 1 ))
c=$(date -d 2017-$a-$b +"%Y%m%d")
echo "/user/developer1/.snapshot/s$c-165612.432"
done
