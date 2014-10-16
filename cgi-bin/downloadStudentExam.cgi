#!/usr/bin/env python

import cgi,sys,os
import cgitb
import subprocess
import uuid
import threading
import time,datetime

cgitb.enable()
dataDir = "../data/"
classesDir = "classes/"
userLockfilesDir = "metadata/lockfiles/"
logDir = "log/"

try:
    form = cgi.FieldStorage()

    remoteUser = form['remoteUser'].value

    # studentDir should be in the form:
    # 'semester/department/course/assignment/studentId/'
    studentDir = form['studentDir'].value
    if remoteUser != os.environ['REMOTE_USER']:
        now = time.strftime("%c")
        with open(dataDir+logDir+'virtualgrade.log','a') as f:
                f.write('UNAUTHORIZED ACCESS ATTEMPT on student grades,'+remoteUser+','+
                         'REAL REMOTE USER:'+os.environ['REMOTE_USER']+','+
                         now+'\n')
        sys.stdout.write("Content-Type: text/html")
        sys.stdout.write("\n")
        sys.stdout.write("\n")
        print 'UNAUTHORIZED. This access will be reported.'
        quit()

except KeyError:
    remoteUser = sys.argv[1]
    studentDir = sys.argv[2]

student = studentDir.split('/')[-2]
assignment = studentDir.split('/')[-3]

assignmentDir = "/".join(studentDir.split('/')[:-2])
studentPDFsFile = dataDir+classesDir+assignmentDir+"/metadata/noStudentPDFs"
        
        
sys.stdout.write("Content-Type: application/pdf\n")
sys.stdout.write("Content-Disposition: attachment; filename="+student+"_"+assignment+".pdf\n");
sys.stdout.write("\n")

if os.path.isfile(studentPDFsFile):
        with open('noExam.pdf',"rb") as pdfFile:
             while 1:
                chunk = pdfFile.read(4096)
                if not chunk: break
                sys.stdout.write (chunk)
        with open("testFile.txt","w") as f:
                f.write("File exists")
        quit()

# update log file
now = time.strftime("%c")
with open(dataDir+logDir+'virtualgrade.log','a') as f:
    f.write('downloadedStudentExam,'+remoteUser+','+
            now+','+student+'\n')

with open(dataDir+classesDir+studentDir+student+'_Full.pdf',"rb") as pdfFile:
     while 1:
        chunk = pdfFile.read(4096)
        if not chunk: break
        sys.stdout.write (chunk)

