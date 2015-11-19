#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys, getopt, os, ConfigParser

from modules import onError, usage, findFiles
from genericpath import isfile

try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'c:p:ro:n:e:vh',
                                 ['configfile=', 'path=', 'recursive', 'oldpattern=', 'newpattern=', 
                                  'extensions=', 
                                  'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

#if len(sys.argv) == 1:  # no options passed
#    onError(2, 2)
    
configFileName = ""
searchPath = os.path.abspath(os.getcwd())
recursive = False
oldPattern = ""
newPattern = ""
extensions = "*"
verbose = False
    
for option, argument in myopts:
    if option in ('-c', '--configfile'):
        configFileName = argument
    elif option in ('-p', '--path'):
        searchPath = os.path.abspath(argument)
    elif option in ('-r', '--recursive'):
        recursive = True
    elif option in ('-o', '--oldpattern'):
        oldPattern = argument
    elif option in ('-n', '--newpattern'):
        newPattern = argument 
    elif option in ('-e', '--extensions'):
        extensions = argument
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)
        
if configFileName: # argument -c --configfile passed
    if not isfile(configFileName): # config file does not exist
        onError(3, "%s is not a valid file" % configFileName)
    if verbose:
        print "\nReading config file...\n"
    myConfig = {}
    with open(configFileName, 'r') as configFile:
        fileContent = configFile.readlines() 
    for line in fileContent:
        if verbose:
            print "Line: %s" % line.rstrip("\n")
        line = line.lstrip(" ")
        #line = line.lower()
        if line.lower().startswith("oldpattern"):
            oldPattern = line.split("=")[1].lstrip(" ").rstrip("\n")
            myConfig['Old pattern'] = oldPattern
        elif line.lower().startswith("newpattern"):
            newPattern = line.split("=")[1].lstrip(" ").rstrip("\n")
            myConfig['New pattern'] = newPattern
        elif line.lower().startswith("searchpath"):
            searchPath = line.split("=")[1].lstrip(" ").rstrip("\n")
            if searchPath.startswith("~"):
                home = os.path.expanduser("~")
                searchPath = ("%s%s") % (home, searchPath.lstrip("~"))
            myConfig['Search path'] = searchPath
        elif line.lower().startswith("recursive"):
            if (line.lower().split("=")[1].lstrip(" ").rstrip("\n") == "yes" or 
                line.split("=")[1].lstrip(" ").rstrip("\n") == "1" or 
                line.lower().split("=")[1].lstrip(" ").rstrip("\n") == "true"):
                recursive = True 
            myConfig['Recursive'] = recursive
            
    if verbose:
        print "\nConfig:"
        for key, value in myConfig.items():
            print "%s: %s" % (key, value)
    
if searchPath:  # argument -p --path passed
    if not os.path.isdir(searchPath):  # not a valid path
        onError(4, "%s is not a valid path" % searchPath)
else:
    print "\nNo path given."
    print "Using current dir %s" % searchPath
        
myFiles = findFiles(searchPath, recursive, extensions, verbose)

toRename = []

for myFile in myFiles:
    if oldPattern in myFile:
        toRename.append(myFile)
        
if toRename:
    print "\nThese files will be renamed:"
    for myFile in toRename:
        print "%s => %s" % (os.path.basename(myFile), os.path.basename(myFile.replace(oldPattern, newPattern)))
                            
                            
                            
                            
                            
                            