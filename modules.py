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
        if extensions == "Videos":
            print "Searching for video files..."
        elif extensions == "Files":
            print "Searching for files only..."
        elif extensions == "*":
            print "Searching for anything..."
    
    if recursive:  # scan directories recursively
        if verbose:
            print "\n--- Searching %s recursively for files matching extension list..." % searchPath
        for root, dirs, files in os.walk(searchPath):
            for myFile in files:
                addFile = False
                if verbose:
                    print "Checking if %s matches..." % myFile
                if extensions == "*Videos":
                    for extension in videoExtensions:
                        if isFile(os.path.join(str(root), myFile), extension):  # check if myFile matches any of the extensions
                            addFile = True
                            break
                elif extensions == "*Subs":
                    for extension in subExtensions:
                        if isFile(os.path.join(str(root), myFile), extension):  # check if myFile matches any of the extensions
                            addFile = True
                            break
                elif extensions == "*Files" and os.path.isfile(myFile) and not os.path.islink(myFile):
                    addFile = True
                elif extensions == "*All":
                    addFile = True
                else:
                    if isFile(os.path.join(str(root), myFile), extensions):
                        addFile = True
                    
                if addFile:
                    if verbose:
                        print "%s matches" % myFile
                    myFiles.append(os.path.join(str(root), myFile))
                    
    else: # scan only given directory
        if verbose:
            print "\n--- Searching %s for files matching extension list..." % searchPath
        for myFile in os.listdir(searchPath):
            addFile = False
            if verbose:
                print "Checking if %s matches..." % myFile
            if extensions == "*Videos":
                for extension in videoExtensions:
                    if isFile(os.path.join(str(searchPath), myFile), extension):  # check if myFile matches any of the extensions
                        addFile = True
                        break
            elif extensions == "*Subs":
                for extension in subExtensions:
                    if isFile(os.path.join(str(searchPath), myFile), extension):  # check if myFile matches any of the extensions
                        addFile = True
                        break
            elif extensions == "*Files" and os.path.isfile(myFile) and not os.path.islink(myFile):
                addFile = True 
            elif extensions == "*All":
                addFile = True
            else:
                if isFile(os.path.join(str(searchPath), myFile), extensions):
                    addFile = True
                
            if addFile:
                if verbose:
                    print "%s matches" % myFile
                myFiles.append(os.path.join(str(searchPath), myFile))
                       
    if verbose:
        print "--- Number of matching files in %s: %d" % (searchPath, len(myFiles))
    
    return sorted(myFiles)

