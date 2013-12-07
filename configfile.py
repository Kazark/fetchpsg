#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Kazark
Created: Dec 7 07
Modified: Aug 31 10
Version: 0.1.1
'''

def readcfg(fileobj):
    '''DOCUMENT'''
    
    lines = fileobj.readlines() # Blank lines are ignored below, not here
    fileobj.close()
    cfg = {}
    
    nl = u'\n' # newline
    crnl = u'\r\n' # carriage return - newline
    cr = u'\r' # carriage return
    
    for line in lines:
    
        # This block of code is a bit tricky, because now that I'm working on
        # this on Linux, we could have mixed newlines in the SFM list file.
        # Thus it requires extra care.
        
        # Ignore blank lines:
        if line in crnl: # This is true if line equals nl, crnl or cr.
            continue
        # Ignore lines that begin with the pound sign, '#'
        if line[0] == '#':
            continue
            
        # Strip newline characters:
        # (The order of these two if statements is important because if we strip
        # the newlines first then we are left with just carriage returns, which
        # do not get stripped. Definitely not what is desired.
        # Also, weird stuff seems to happen anyway, so I also check for carriage
        # return alone.
        if line[-2:] == u'\r\n':
            line = line[:-2]
        if line[-1] == nl or line[-1] == cr:
            # I don't know why it would ever equal cr, but it seems to happen.
            line = line[:-1]
            
        # Parse:
        lst = line.split('=') # Separate the field names and the markers
        cfg[lst[0]] = lst[1]
        # We need this to allow us to call the field and return the sfm marker.
    
    return cfg
    
