#!/usr/bin/env python
import cgi,sys,os
import cgitb
import json
import uuid

cgitb.enable()
dataDir = "../data/"

# loads new page and sets all POSTed (or GET) keys to their value inside the javascript of the file
def loadNewPage(page,form):
    # TODO: Authenticate user
    # ...if userInfo['id']=='106628659834464477412':
    # read in setupAssignment.html and print it to the screen
    with open("html/"+page+".html","r") as f:
        for line in f:
            foundKey=False
            for key in form.keys():
                if line.startswith("var "+key+" = '';"):
                    try:
                        formValue = form[key].value # if this is a cgiforms form
                    except:
                        formValue = form[key] # if this is a regular dictionary
                    print("var "+key+" = '"+formValue+"';")
                    foundKey=True
                    break
            if not foundKey:
                sys.stdout.write(line)

if __name__ == "__main__":
    form = cgi.FieldStorage()

    try:
            page=form['page'].value
            formKeys = list(form.keys())
            formKeys.pop(formKeys.index('page'))    
    except:
            print "Location: https://www.eecs.tufts.edu/~cgregg/grades\n"

    sys.stdout.write("Content-Type: text/html")
    sys.stdout.write("\r\n")
    sys.stdout.write("\r\n")
    
    #userToken = form['userToken'].value
    if page=='startGradeReport':
        loadNewPage('gradeReport',form)
    else:
        print page+"<p>"
        sys.stdout.write("Unauthorized.\n")



