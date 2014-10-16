#!/usr/bin/env python

import cgi,sys,os
import shutil
import cgitb
import subprocess
import uuid
import threading
import time,datetime
import json

cgitb.enable()
dataDir = "../data/"
classesDir = "classes/"
userLockfilesDir = "metadata/lockfiles/"
logDir = "log/"
metadataDir = "metadata/"
baseDirLen = len((dataDir+classesDir).split('/'))-1

try:
    form = cgi.FieldStorage()
    remoteUser = form['remoteUser'].value
    if remoteUser != os.environ['REMOTE_USER']:
        now = time.strftime("%c")
        with open(dataDir+logDir+'virtualgrade.log','a') as f:
                f.write('UNAUTHORIZED ACCESS ATTEMPT on student grades,'+remoteUser+','+
                         'REAL REMOTE USER:'+os.environ['REMOTE_USER']+','+
                         now+'\n')
        sys.stdout.write("Content-Type: application/json")
        sys.stdout.write("\n")
        sys.stdout.write("\n")
        print json.dumps('UNAUTHORIZED. This access will be reported.')
        quit()
except KeyError:
    remoteUser = sys.argv[1]
        
# load grades from allGrades.txt file

with open(dataDir+"allGrades.txt","r") as f:
        assignmentDataList = json.loads(f.read())

studentData = []
for assignment in assignmentDataList:
        if assignment['student'] == remoteUser:
               studentData.append(assignment)
               
# update log file
now = time.strftime("%c")
with open(dataDir+logDir+'virtualgrade.log','a') as f:
    f.write('retrieveGrades,'+remoteUser+','+
            now+'\n')
            
sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")
print json.dumps(studentData)


