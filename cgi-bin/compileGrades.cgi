#!/usr/bin/env python

import cgi,sys,os
import shutil
import cgitb
import subprocess
import uuid
import time,datetime
import json

dataDir = "../data/"
classesDir = "classes/"
userLockfilesDir = "metadata/lockfiles/"
logDir = "log/"
metadataDir = "metadata/"
baseDirLen = len((dataDir+classesDir).split('/'))-1

# traverse root directory, and list directories as dirs and files as files
dirStructure = []
for root, dirs, files in os.walk(dataDir+classesDir):
        #dirStructure.append(root+'/'+remoteUser)
        for dir in dirs:
                if dir=='metadata': continue
                if dir=='lockfiles': continue
                # check for first page graded (meaning that the grade exists)
                gradedPage1 = root+'/'+dir+'/metadata/'+'page1_totalGrade.png'
                if os.path.isfile(gradedPage1):
                     dirStructure.append(root+'/'+dir)

assignmentDataList = []
for assignment in dirStructure:
        assignmentData = {}
        fullMetadataDir = '/'.join(assignment.split('/')[:-1])+'/metadata/'
        if os.path.exists(fullMetadataDir+'published'):
                # grades have been published
                try:
                        with open(fullMetadataDir+'assignmentName.txt','r') as f:
                                assignmentData['assignmentName']=f.readline()[:-1]
                except IOError:
                        assignmentData['assignmentName']=''
                assignmentParts = assignment.split('/')
                assignmentData['semester']=assignmentParts[3]
                assignmentData['department']=assignmentParts[4]
                assignmentData['class']=assignmentParts[5]
                assignmentData['assignment']=assignmentParts[6].split('_')[-1]
                assignmentData['student']=assignmentParts[7]
                
                gradeFiles = os.listdir(assignment+'/metadata/')
                studentScore = 0
                totalPoints = 0
                for gradeFile in gradeFiles:
                        if '.grd' in gradeFile:
                                with open(assignment+'/metadata/'+gradeFile,"r") as f:
                                        line = f.readline()[:-1].split(',')
                                        studentScore+=float(line[0])
                                        totalPoints+=float(line[4])
                                assignmentData['score']=studentScore
                                assignmentData['totalPoints']=totalPoints
                assignmentDataList.append(assignmentData)

with open(dataDir+'allGrades.txt', 'w') as outfile:
        json.dump(assignmentDataList, outfile)
