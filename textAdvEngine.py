#!/usr/bin/env python
import re

# First, open the locale attributes file.
localeSource = open('localeAttributes.txt', 'r')

# Now define the list of strings for the "Here be monsters" shortDesc.

hereBeFile = open('hereBeMonsters.txt', 'r')
hereBeList = []
for line in hereBeFile:
    hereBeList.append(line)

# print hereBeList

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

# To find the number of locales, we need to know how many entries each locale has, and divide the length of newInitialList by that...and by two--one entry is two elements, the eventual key-value pair.

numAttr = 9 #The number of attributes each locale has.

numLocales = len(newInitialList) / numAttr / 2

# print "There are %f locales." % numLocales

# Now create the final list with nxn lists nested inside.
# 110310: Rather than just creating numbers, we'll use the value of *scaryLandDesc* as the default. This way the full map is preset and we only need add more locales to flesh it out. BRILLIANT MOTHER FUCKER!

finalList = []

for i in range(numLocales):
    finalList.append([])
    for j in range(numLocales):
#        finalList[i].append(j)
        if not ignorePattern.search(hereBeList[j % len(hereBeList)]):
            # Amending this to indicate the "hereBeMonsters" locales are off-limits. Will compare x attribute later. 
            finalList[i].append({'x' : -1, 'shortDesc' : hereBeList[j % len(hereBeList)].rstrip('\n').lstrip()})
        elif not ignorePattern.search(hereBeList[j % len(hereBeList) + 1]):
            finalList[i].append({'x' : -1, 'shortDesc' : hereBeList[j % len(hereBeList) + 1].rstrip('\n').lstrip()})
        else:
            finalList[i].append({'x' : -1, 'shortDesc' : hereBeList[j % len(hereBeList) + 2].rstrip('\n').lstrip()})
        

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

 #                        print newInitialList[n] + "=" + newInitialList[n+1]
 #                        print newInitialList[n+2] + "=" + newInitialList[n+3]
 #                        print newInitialList[n+4] + "=" + newInitialList[n+5]
 #                        print newInitialList[n+6] + "=" + newInitialList[n+7]
 #                        print newInitialList[n+8] + "=" + newInitialList[n+9]
 #                        print newInitialList[n+10] + "=" + newInitialList[n+11]
 #                        print newInitialList[n+12] + "=" + newInitialList[n+13]
 #                        print newInitialList[n+14] + "=" + newInitialList[n+15]
 #                        print newInitialList[n+16] + "=" + newInitialList[n+17]
                        # print intermeDict
                        # for k, v in intermeDict:
                        #     print "The value of %s is %s." % (k, v)
                        # print intermeDict
                        finalList[i][j] = intermeDict 


print finalList

# Need to experiment to be able to return any locale attribute. Currently, these are stored as key-value pairs.

# print """
# 
# 
# 
# """
# print finalList[0][0]
# print """
# 
# 
# 
# """
# print finalList[0][0]['x']
# 110921 Initial stab at navigation. Use while loop to maintain persistence, exiting on "QUIT."
# 110922 Problem is, the locales that are off-limit exist, so are iterable, but don't have "longDesc" keys. Need to check not only for whether the chosen direction is in-scope, but also if it has "longDesc".
#        Fixed.

initialPosition = [0,0]
print finalList[initialPosition[0]][initialPosition[1]]["longDesc"]
position = initialPosition
directive = raw_input('Where will you go? \n')
print len(finalList)
print len(finalList[0])
# directive = "QUIT"
while directive != "QUIT":
    # Need to parse 'directive' for directions
    if directive == "N":
        if position[1] == 0:
            print "You can't go that way asshole."
        elif finalList[position[0]][position[1] - 1]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0]][position[1] - 1]["shortDesc"]
        else:
            position[1] -= 1
            print finalList[position[0]][position[1]]["longDesc"]
    elif directive == "S":
        if position[1] == len(finalList):
            print "You can't go that way asshole."
        elif finalList[position[0]][position[1] + 1]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0]][position[1] + 1]["shortDesc"]
        else:
            position[1] += 1
            print finalList[position[0]][position[1]]["longDesc"]
    elif directive == "E":
        if position[0] == len(finalList[0]):
            print "You can't go that way asshole."
        elif finalList[position[0] + 1][position[1]]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0] + 1][position[1]]["shortDesc"]
        else:
            position[0] += 1 
            print finalList[position[0]][position[1]]["longDesc"]
    elif directive == "W":
        if position[0] == 0:
            print "You can't go that way asshole."
        elif finalList[position[0] - 1][position[1]]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0] - 1][position[1]]["shortDesc"]
        else:
            position[0] -= 1
            print finalList[position[0]][position[1]]["longDesc"]

    directive = raw_input('Where will you go? \n')
