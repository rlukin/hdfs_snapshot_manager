#! /usr/bin/python

import subprocess
import re
import time
import pprint

def get_snapshots_dict():
#    command = ["hdfs", "dfs", "-ls", "-C", "/user/*/.snapshot"]
    command = ["/home/hdfs/gendate.sh", "100"]
    snapshots = subprocess.check_output(command)
    snapshots = snapshots.splitlines()
    
    snapshots_dict = {}
    
    for snapshot in snapshots:
        raw_date = re.search('(?<=.snapshot/s)[0-9]+', snapshot).group(0)
        epoch = time.mktime(time.strptime(raw_date, "%Y%m%d"))
        snapshots_dict.update({snapshot: epoch})
    return snapshots_dict

def print_snapshot_groups(weekly, monthly, old, redundant):
    pp = pprint.PrettyPrinter(indent=4)
    
    print '-'*((80-25)/2),'under week ago snapshots:','-'*((80-25)/2)
    pp.pprint(weekly)
    
    print '-'*((80-7)/2),'monthly','-'*((80-7)/2)
    pp.pprint(monthly)
    
    print '-'*((80-16)/2),'older than month','-'*((80-16)/2-1)
    pp.pprint(old)

    print '-'*((80-18)/2),'snapshots to remove','-'*((80-18)/2)
    pp.pprint(redundant)

def get_redundant(array, period):
    redundant = []
    latest = array[0][1]
    array = array[1:]
    for item in array:
        if (item[1] <= latest - period):
           latest = item[1]
        else:
          redundant.append(item[0])
    return redundant


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

weekly_snapshots.sort(key=lambda x: x[1], reverse=True)
monthly_snapshots.sort(key=lambda x: x[1], reverse=True)
old_snapshots.sort(key=lambda x: x[1], reverse=True)

redundant_snapshots = get_redundant(monthly_snapshots, week) + get_redundant(old_snapshots, month) 

print_snapshot_groups(weekly_snapshots, monthly_snapshots, old_snapshots, redundant_snapshots)

weekly_snapshots = [ x for x in weekly_snapshots if x[0] not in redundant_snapshots]
monthly_snapshots = [ x for x in monthly_snapshots if x[0]  not in redundant_snapshots]
old_snapshots = [ x for x in old_snapshots if x[0] not in redundant_snapshots]


print "After removing unnecessary files we have only:"
print_snapshot_groups(weekly_snapshots, monthly_snapshots, old_snapshots, None)
