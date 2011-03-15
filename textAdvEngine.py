#!/usr/bin/env python
import re

# First, open the locale attributes file.
localeSource = open('localeAttributes.txt', 'r')

# Now define the list of strings for the "Here be monsters" shortDesc.

hereBeFile = open('hereBeMonsters.txt', 'r')
hereBeList = []
for line in hereBeFile:
    hereBeList.append(line)

print hereBeList

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

# print initialList

# Now this list is kinda janky: each line was split into a two-term list. The crappy algorithm I came up with uses a single list, where each pair-of-interest is comprised of sequential terms. We need to make this.

newInitialList = []

for littleList in initialList:
    for n in range(2):
        newInitialList.append(littleList.pop(0).rstrip('\n').lstrip())
        
        # print littleList[n]

# print newInitialList

# With the list now as we'd like it, it's time to build the list of lists of dictionaries. Thing is, as we can't insert items into a list into arbitrary indices, we need to create the nested lists with a conservative number of spots. We'll use the number of locales n and create what amounts to an nxn matrix--n lists with n terms each. Of course, this will be overly large, so we may thereafter need to remove items, for performance. But, actually, we're not using nested lists for performance.

# To fine the number of locales, we need to know how many entries each locale has, and divide the length of newInitialList by that...and by two--one entry is two elements, the eventual key-value pair.

numAttr = 9 #The number of attributes each locale has.

numLocales = len(newInitialList) / numAttr / 2

print "There are %f locales." % numLocales

# Now create the final list with nxn lists nested inside.
# 110310: Rather than just creating numbers, we'll use the value of *scaryLandDesc* is the default. This way the full map is preset and we only need add more locales to flesh it out. BRILLIANT MOTHER FUCKER!

finalList = []

for i in range(numLocales):
    finalList.append([])
    for j in range(numLocales):
#        finalList[i].append(j)
        if not ignorePattern.search(hereBeList[j % len(hereBeList)]):
            finalList[i].append({'shortDesc' : hereBeList[j % len(hereBeList)].rstrip('\n').lstrip()})
        elif not ignorePattern.search(hereBeList[j % len(hereBeList) + 1]):
            finalList[i].append({'shortDesc' : hereBeList[j % len(hereBeList) + 1].rstrip('\n').lstrip()})
        else:
            finalList[i].append({'shortDesc' : hereBeList[j % len(hereBeList) + 2].rstrip('\n').lstrip()})
        

# print finalList

# Now...to populate the list. The most difficult part will be pulling the 2*numLocales entries from newInitialList and creating a dictionary out of them. Or will it?

print len(newInitialList)
# for m in range(len(newInitialList)):
#     print newInitialList.pop(m)

for i in range(numLocales):
    for j in range(numLocales):
        for n in range(len(newInitialList)):
            if newInitialList[n] == "x" and \
                    newInitialList[n+1] == str(j) and \
                    newInitialList[n+2] == "y" and \
                    newInitialList[n+3] == str(i):
                        # print "The things in order are:" +  '\n' + \
                        # newInitialList[n] + "=" +  newInitialList[n+1] + '\n' + \
                        # newInitialList[n+2] + "=" + newInitialList[n+3] + '\n' + \
                        # newInitialList[n+4] + "=" + newInitialList[n+5] + '\n' + \
                        # newInitialList[n+6] + "=" + newInitialList[n+7] + '\n'
                        intermeDict = {}
                        intermeDict[newInitialList[n]]=newInitialList[n+1]
                        intermeDict[newInitialList[n+2]]=newInitialList[n+3]
                        intermeDict[newInitialList[n+4]]=newInitialList[n+5]
                        intermeDict[newInitialList[n+6]]=newInitialList[n+7]
                        intermeDict[newInitialList[n+8]]=newInitialList[n+9]
                        intermeDict[newInitialList[n+10]]=newInitialList[n+11]
                        intermeDict[newInitialList[n+12]]=newInitialList[n+13]
                        intermeDict[newInitialList[n+14]]=newInitialList[n+15]
                        intermeDict[newInitialList[n+16]]=newInitialList[n+17]

                        print newInitialList[n] + "=" + newInitialList[n+1]
                        print newInitialList[n+2] + "=" + newInitialList[n+3]
                        print newInitialList[n+4] + "=" + newInitialList[n+5]
                        print newInitialList[n+6] + "=" + newInitialList[n+7]
                        print newInitialList[n+8] + "=" + newInitialList[n+9]
                        print newInitialList[n+10] + "=" + newInitialList[n+11]
                        print newInitialList[n+12] + "=" + newInitialList[n+13]
                        print newInitialList[n+14] + "=" + newInitialList[n+15]
                        print newInitialList[n+16] + "=" + newInitialList[n+17]
                        # print intermeDict
                        # print intermeDict
                        # for k, v in intermeDict:
                        #     print "The value of %s is %s." % (k, v)
                        # print intermeDict
                        finalList[i][j] = intermeDict 


print finalList

# You see, this works nicely now...except. Except for the fact that we have extraneous terms, the filler terms. Maybe instead of numbers I should prime finalList with empty strings. 

# There are various ways to pop those elements out. We might try to use the .items() method and catching the AttributeError when we hit an element that's not a dictionary. Else, we can use isinstance(var, dict) to see if the element is an instance of a particular class (in this case, the dict class). We use the latter here.

# Dilemma: how to iterate over the lists of dictionaries and numbers to remove the numbers. Sure, we can use the length of the list, but we'll create indices larger than the length once we pop entries. Right?

# Also, there's the issue that there may be (and in our test case are) lists without any localeEntries in them. So not only do we need to remove terms from lists, we need to remove whole lists. Unless...

# ...unless we don't put numbers in our seed "array" but rather something like "Here be monsters." That way, we can check dynamically against that, and it fits the game. We'll need a similar boundary condition for the entire map.

# What if we initialize the entire map, for the entire known world, and use "Here be monsters" as the filler information? Even use "{'shortDesc': 'Here be monsters." for all those spaces we may yet fill? YES!

# for i in len(finalList):
#     for j in len
