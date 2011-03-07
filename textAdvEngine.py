#!/usr/bin/env python
import re

# First, open the locale attributes file.
localeSource = open('localeAttributes.py','r')

# Now populate the list of lists of dicts with locale data.
# First, compile the search pattern for comments and empty lines.
ignorePattern = re.compile('^#\s\w.|^\n')
scrubNewLines = re.compile('^.*')

# Declare the lists we'll need. There is almost certainly a better way to ensure we have enough space and won't run out of indices, but this will suffice.

initialList=[]
innerList = []
finalList = []

for line in localeSource:
    if not ignorePattern.search(line):
        # some code that parses crap or whatever, returning a list of
        # lists of dictionaries, e.g., [{'x': 0, 'y': 0, 'desc': '...'},...]

        # The first pass will simply populate the list; then we'll
        # need to logically sort it, so that the list indices distribute
        # as the coordinates.
        
        initialList.append(re.split(':', line))

print initialList

# Now this list is kinda janky: each line was split into a two-term list. The crappy algorithm I came up with uses a single list, where each pair-of-interest is comprised of sequential terms. We need to make this.

newInitialList = []

for littleList in initialList:
    for n in range(2):
        newInitialList.append(littleList.pop(0).rstrip('\n').lstrip())
        
        # print littleList[n]

# With the list now as we'd like it, 


print newInitialList
