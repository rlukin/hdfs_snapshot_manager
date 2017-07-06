#! /usr/bin/python

import subprocess
import re
import time

def get_snapshots_dict():
#    command = ["hdfs", "dfs", "-ls", "-C", "/user/*/.snapshot"]
    command = ["/home/hdfs/gendate.sh", "30"]
    snapshots = subprocess.check_output(command)
    snapshots = snapshots.splitlines()
    
    snapshots_dict = {}
    
    for snapshot in snapshots:
        raw_date = re.search('(?<=.snapshot/s)[0-9]+', snapshot).group(0)
        epoch = time.mktime(time.strptime(raw_date, "%Y%m%d"))
        snapshots_dict.update({snapshot: epoch})
    return snapshots_dict


week = 7*24*60*60
month = 30*24*60*60

current_time = time.time()
week_ago = current_time - week
month_ago = current_time - month

weekly_snapshots = []
monthly_snapshots = []
old_snapshots = []

snapshots = get_snapshots_dict()

for snapshot, date in snapshots.items():
    if (date >= week_ago):
        weekly_snapshots.append([snapshot, date])
    elif (date < week_ago) and (date >= month_ago):
        monthly_snapshots.append([snapshot, date])
    elif (date < month_ago):
        old_snapshots.append([snapshot, date])

print weekly_snapshots
print '+'*80
print monthly_snapshots
print '+'*80
print old_snapshots

print current_time, week_ago, month_ago
