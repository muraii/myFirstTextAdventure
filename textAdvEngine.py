#!/usr/bin/env python
import re

# First, open the locale attributes file.
localeSource = open('localeAttributes.txt', 'r')

# Break for debugging...
wait=raw_input("Enter a key to continue. Like, literally.")

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

# Now define the list of strings for the "Here be monsters" shortDesc.
hereBeList = []
hereBeList.append([]) # List to contain hereBe_surface descriptions.
hereBeList.append([]) # List to contain hereBe_tier1 descriptions.
hereBeList.append([]) # List to contain hereBe_tier2 descriptions.
hereBeFileList = []

hereBeFile_surface = open('hereBe_surface', 'r')
hereBeFile_tier1 = open('hereBe_tier1', 'r')
hereBeFile_tier2 = open('hereBe_tier2', 'r')

hereBeFileList.append(hereBeFile_surface)
hereBeFileList.append(hereBeFile_tier1)
hereBeFileList.append(hereBeFile_tier2)

for i in range(3):
    for line in hereBeFileList[i]:
        hereBeList[i].append(line)

# print hereBeList
# for scaryList in hereBeList:
#     print scaryList

# wait = raw_input('Break now.')
# To make our tiled world 3D, need to fill out finalList on x, y, and z axes. To do that, we want 
# print hereBeList
# for place in hereBeList:
#     print place

# Now create the final list with nxn lists nested inside.
# 110310: Rather than just creating numbers, we'll use the value of *scaryLandDesc* as the default. This way the full map is preset and we only need add more locales to flesh it out. BRILLIANT MOTHER FUCKER!

finalList = []

for i in range(numLocales):
    finalList.append([])
    for j in range(numLocales):
        finalList[i].append([])
        for k in range(numLocales):
            # Need to start at j + 2 to account for the two lines of instructions in hereBeMonsters.txt
            # Always need to maintain numLocales > len(hereBeList) + 2
            # Will checking "j % len(hereBeList -2) + 2" fix that? Should. [DOES]
            if k < 2:
                if not ignorePattern.search(hereBeList[k][k % (len(hereBeList) - 2) + 2]):
                    # Amending this to indicate the "hereBeMonsters" locales are off-limits. Will compare x attribute.
                    finalList[i][j].append({'x' : -1, 'ijk': "%i %i %i" % (i, j, k),  'shortDesc' : hereBeList[k][i % (len(hereBeList) - 2) + 2].rstrip('\n').lstrip()})
            else:
                if not ignorePattern.search(hereBeList[2][k % (len(hereBeList) - 2) + 2]):
                    # Amending this to indicate the "hereBeMonsters" locales are off-limits. Will compare x attribute.
                    finalList[i][j].append({'x' : -1, 'ijk': "%i %i %i" % (i, j, k),  'shortDesc' : hereBeList[2][i % (len(hereBeList) - 2) + 2].rstrip('\n').lstrip()})


for i in range(numLocales):
    for j in range (numLocales):
        # print "(%i, %i)" % (i, j),
        print finalList[j][i]

wait = raw_input('Break now.')
# print "This is the final list."
# print finalList

# Now...to populate the list. The most difficult part will be pulling the 2*numLocales entries from newInitialList and creating a dictionary out of them. Or will it?

# print len(newInitialList)
# for m in range(len(newInitialList)):
#     print newInitialList.pop(m)

for i in range(numLocales):
    for j in range(numLocales):
        for k in range(numLocales):
            # 110923 Going to try adding third dimension.
            for n in range(len(newInitialList)):
                if newInitialList[n] == "x" and \
                        newInitialList[n+1] == str(k) and \
                        newInitialList[n+2] == "y" and \
                        newInitialList[n+3] == str(j) and \
                        newInitialList[n+4] == "z" and \
                        newInitialList[n+5] == str(i):
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
                            intermeDict[newInitialList[n+18]]=newInitialList[n+19]
    
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
                            # Note x->j and y->i
                            # finalList[j][i] = intermeDict 
                            finalList[k][j][i] = intermeDict 


for i in range(numLocales):
    for j in range (numLocales):
        # print "(%i, %i)" % (i, j),
        for k in range(numLocales):
            print "%i, %i, %i:" % (k, j, i), finalList[k][j][i]
            wait=raw_input("Dude there are a lot of these.")

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

initialPosition = [0,0,0]
print finalList[initialPosition[0]][initialPosition[1]][initialPosition[2]]["longDesc"]
# initialPosition = [0,0]
# Note that the coordinate in finalList is effectively (y, x), so ensure the indices are used this way.
# print finalList[initialPosition[1]][initialPosition[0]]["longDesc"]
position = initialPosition
directive = raw_input('Where will you go? \n')
# print len(finalList)
# print len(finalList[0])
# directive = "QUIT"
while directive != "QUIT":
    # Need to parse 'directive' for directions
    if directive == "N":
        if position[1] == 0:
            print "You can't go that way asshole."
        elif finalList[position[0]][position[1] - 1][position[2]]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0]][position[1] - 1][position[2]]["shortDesc"]
        else:
            position[1] -= 1
            print finalList[position[0]][position[1]][position[2]]["longDesc"]
    elif directive == "S":
        if position[1] == numLocales - 1:
            print "You can't go that way asshole."
        elif finalList[position[0]][position[1] + 1][position[2]]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0]][position[1] + 1][position[2]]["shortDesc"]
        else:
            position[1] += 1
            print finalList[position[0]][position[1]][position[2]]["longDesc"]
    elif directive == "E":
        if position[0] == numLocales - 1:
            print "You can't go that way asshole."
        elif finalList[position[0] + 1][position[1]][position[2]]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0] + 1][position[1]][position[2]]["shortDesc"]
        else:
            position[0] += 1 
            print finalList[position[0]][position[1]][position[2]]["longDesc"]
    elif directive == "W":
        if position[0] == 0:
            print "You can't go that way asshole."
        elif finalList[position[0] - 1][position[1]][position[2]]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0] - 1][position[1]][position[2]]["shortDesc"]
        else:
            position[0] -= 1
            print finalList[position[0]][position[1]][position[2]]["longDesc"]
    elif directive == "U":
        if position[2] == numLocales - 1: 
            print "You can't go that way asshole."
        elif finalList[position[0]][position[1]][position[2] + 1]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0]][position[1]][position[2] + 1]["shortDesc"]
        else:
            position[2] += 1 
            print finalList[position[0]][position[1]][position[2]]["longDesc"]
    elif directive == "D":
        if position[2] == 0:
            print "You can't go that way asshole."
        elif finalList[position[0]][position[1]][position[2] - 1]["x"] == -1:
            print " %s \n You cannot go that way." % finalList[position[0]][position[1]][position[2] - 1]["shortDesc"]
        else:
            position[2] -= 1
            print finalList[position[0]][position[1]][position[2]]["longDesc"]

    directive = raw_input('Where will you go? \n')


# State 110923 : 11:33
# So, tried doing 3D. After realizing it should optimally require a redesign of the indexing scheme, I went back to 2D. Now I realize the 'hereBeMonsters' stuff doesn't fill as neatly as I thought. As it is now, the balance of column 1 and all of columns 2-4 are filled with the same text, and then column 5 is filled with a different one. I intended the finalList to be initialized with iterated descriptions.
# I see that I will need to have stricter standards for the localeAttributes listings. Here are some improvements I have in mind:
#   create locales specifically for the out-of-bounds areas
#   use a field to distinguish more clearly the out-of-bounds areas
#   use locale coordinates to place information rather than rely on their position in the source file
#       (This provides for more flexibility in the source file, as locales can be added without worrying about position, though this may just be sloppy/lazy)
#   build an xy plane for each unit of z
#   replace nested IF structure with dict that maps compass direction to offset
# State 110923 : 12:41
# Keep hereBeMonsters for list initialization, but will definitely need to have strict standards for localeAttributes listings. This allows for testing play with an incomplete map without running out of scope. The goal is to fill all tiles with authored content. Definitely need to consider a different filler strategy for the z axis; going up shouldn't be meet a "deep impassible fissure." Conditional use of filler? Lord that could get messy
# Except...yeah. hereBeMonsters becomes a list of lists. This allows for expandability as I allow for tall structures, stairways, etc. Definitely this is happening maybe. Similarly, locale definitions must be multilayered.
