#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import ConfigParser, os, sys
from __builtin__ import False

config = ConfigParser.ConfigParser()  # define config file
config.read("%s/config.ini" % os.path.dirname(os.path.realpath(__file__)))  # read config file

videoExtensions = (config.get('fileTypes', 'videoExtensions').replace(" ", "")).split(',')  # load video extensions
subExtensions = (config.get('fileTypes', 'subExtensions').replace(" ", "")).split(',')  # load subtitle extensions


def onError(errorCode, extra):
    print "\nError: %s" % errorCode
    if errorCode in (1, 4):
        print extra
        usage(errorCode)
    elif errorCode in (3, 5):
        print "%s" % extra
        sys.exit(errorCode)
    elif errorCode == 2:
        print "No options given"
        usage(errorCode)
    elif errorCode in (6, 7, 8, 9):
        print "%s" % extra
        
def usage(exitCode):
    print "\nUsage:"
    print "----------------------------------------"
    print "%s " % sys.argv[0]

    sys.exit(exitCode)
    
def isFile(myFile, extension):
    result = False
    fileExtension = os.path.splitext(myFile)[1]
    if fileExtension.lower() == ".%s" % extension:
        result = True
    return result
    
def findFiles(searchPath, recursive, extensions, verbose):
    myFiles = []
    if verbose:
        print "\n"
        if extensions.lower() == "videos":
            print "--- Searching for video files..."
        elif extensions.lower() == "files":
            print "--- Searching for files only..."
        elif extensions.lower() == "*files":
            print "--- Searching for anything..."
        else:
            print "--- Searching for files with extensions: %s" % extensions.lower()
    
    if recursive:  # scan directories recursively
        if verbose:
            print "\n--- Searching %s recursively for files matching extension list..." % searchPath
        for root, dirs, files in os.walk(searchPath):
            for myFile in files:
                addFile = False
                if verbose:
                    print "--- Checking if %s matches..." % os.path.join(str(root), myFile)
                if extensions.lower() == "*ideos":
                    for extension in videoExtensions:
                        if verbose:
                            print "--- Checking extension %s ..." % extension 
                        if isFile(os.path.join(str(root), myFile), extension):  # check if myFile matches any of the extensions
                            addFile = True
                            break
                elif extensions.lower() == "*subs":
                    for extension in subExtensions:
                        if verbose:
                            print "--- Checking extension %s ..." % extension
                        if isFile(os.path.join(str(root), myFile), extension):  # check if myFile matches any of the extensions
                            addFile = True
                            break
                elif extensions.lower() == "*files" and os.path.isfile(os.path.join(str(root), myFile)) and not os.path.islink(myFile):
                    addFile = True
                elif extensions.lower() == "*all":
                    addFile = True
                else:
                    for extension in (extensions.replace(" ", "")).split(','):
                        if verbose:
                            print "--- Checking extension %s ..." % extension
                        if isFile(os.path.join(str(root), myFile), extension):
                            addFile = True
                            break
                    
                if addFile:
                    if verbose:
                        print "+++ %s matches" % myFile
                    myFiles.append(os.path.join(str(root), myFile))
                    
    else: # scan only given directory
        if verbose:
            print "\n--- Searching %s for files matching extension list..." % searchPath
        for myFile in os.listdir(searchPath):
            addFile = False
            if verbose:
                print "--- Checking if %s matches..." % os.path.join(str(searchPath), myFile)
            if extensions.lower() == "*videos":
                for extension in videoExtensions:
                    if verbose:
                        print "--- Checking extension %s ..." % extension
                    if isFile(os.path.join(str(searchPath), myFile), extension):  # check if myFile matches any of the extensions
                        addFile = True
                        break
            elif extensions.lower() == "*subs":
                for extension in subExtensions:
                    if verbose:
                        print "--- Checking extension %s ..." % extension
                    if isFile(os.path.join(str(searchPath), myFile), extension):  # check if myFile matches any of the extensions
                        addFile = True
                        break
            elif extensions.lower() == "*files" and os.path.isfile(os.path.join(str(searchPath), myFile)) and not os.path.islink(myFile):
                addFile = True 
            elif extensions.lower() == "*all":
                addFile = True
            else:
                for extension in (extensions.lower().replace(" ", "")).split(','):
                    if verbose:
                        print "--- Checking extension %s ..." % extension
                    if isFile(os.path.join(str(searchPath), myFile), extension):
                        addFile = True
                        break
                
            if addFile:
                if verbose:
                    print "+++ %s matches" % myFile
                myFiles.append(os.path.join(str(searchPath), myFile))
                       
    if verbose:
        print "--- Number of matching files in %s: %d" % (searchPath, len(myFiles))
        print "File list:"
        for line in myFiles:
            print line
    
    return sorted(myFiles)

def doRename(myFile, newName, yesToQuestions, verbose):
    runRename = False
    
    if yesToQuestions:
        if verbose:
            print
        runRename = True
    else:
        print '\nDo you want to rename\n%s to\n%s ?' % (myFile, newName)
        answer = raw_input('(y/N/q)')
        if answer.lower() =="y":
            runRename = True
        elif answer.lower() == "q":
            print "\n--- Quitting..."
            sys.exit(0)
        else:
            print "*** Skipping this file"
        
    if runRename:
        writeAccess = True
        if verbose:
            print "--- Checking permissions..."
        if not os.access(myFile, os.W_OK):
            onError(6, "*** You don't have write permission to %s\n    Skipping..." % myFile)
            writeAccess = False
        if not os.access(os.path.dirname(newName), os.W_OK):
            onError(7, "*** You don't have write permission to directory %s\n    Skipping..." % os.path.dirname(newName))
            writeAccess = False
        

    if runRename and writeAccess:
        if verbose:
            print "--- Renaming\n    %s    to\n    %s" % (myFile, newName)
        os.rename(myFile, newName)
        
        if verbose:
            print "--- Checking after renaming..."
        if os.path.exists(myFile):
            onError(8, "*** Failed deleting %s\n    Look this up!" % myFile)
        if not os.path.exists(newName):
            onError(9, "*** Failed creating %s\n    Look this up!" % myFile)
        


