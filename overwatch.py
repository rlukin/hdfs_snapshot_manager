#! /usr/bin/python

import subprocess
import re
from pprint import pprint

import dateutil.relativedelta
from datetime import datetime

def get_snapshots():
    
    #get snapshot list from hdfs /user 

    #command = ["hdfs", "dfs", "-ls", "-C", "/user/*/.snapshot"]
    command = ["/home/vagrant/gendate.sh"]
    snapshots = subprocess.check_output(command)
    snapshots = snapshots.splitlines()
    
    snapshots.sort()
    return snapshots

def get_snapshot_date(name):

    #convert snapshot name to date

    raw_date = re.search('(?<=.snapshot/s)[0-9]+', name).group(0)
    date = datetime.strptime(raw_date, "%Y%m%d")
    return date

def get_outdated(snapshots):
    
    #apply backup policy
    #determ useless backups
    
    #define passed week and month
    week  = datetime.now() - dateutil.relativedelta.relativedelta(days=7)
    month = datetime.now() - dateutil.relativedelta.relativedelta(months=1)

    outdated = []

    for snapshot in snapshots:
        snapshot_date = get_snapshot_date(snapshot)
        
        #rule for passed month backup
        #keep friday release backups 
        if ( snapshot_date < week) and (snapshot_date > month):
            if ( snapshot_date.isoweekday() != 5 ) and ( snapshot_date.day != 1 ):
                outdated.append(snapshot)

        #rule for older than month backups
        #keep first day of month copy
        if ( snapshot_date <= month):
            if ( snapshot_date.day != 1 ):
                outdated.append(snapshot)
         
    return outdated

def remove_snapshots(snapshots):
    for snapshot in snapshots:
        command = ["hdfs", "dfs", "-deleteSnapshot", snapshot]
        subprocess.call(command)


snapshots = get_snapshots()

outdated_snapshots = get_outdated(snapshots)

#remove_snapshots(outdated_snapshots)    

print "After removing unnecessary files we have only:"
pprint([ x for x in snapshots if x not in outdated_snapshots ])
