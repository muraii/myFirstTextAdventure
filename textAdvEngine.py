#!/usr/bin/env python
import re
import readline # This allows raw_input() to understand backspaces
readline # Here just to make the real-time parser think I'm using the module, so it won't highlight the import as a syntax error.


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

print "Here is initialList."
print initialList
print "Here was initialList."

# Now this list is kinda janky: each line was split into a two-term list. The crappy algorithm I came up with uses a single list, where each pair-of-interest is comprised of sequential terms. We need to make this.

newInitialList = []

for littleList in initialList:
    for n in range(2):
        newInitialList.append(littleList.pop(0).rstrip('\n').lstrip())
        
        # print littleList[n]

# print newInitialList

# With the list now as we'd like it, it's time to build the list of lists of dictionaries. Thing is, as we can't insert items into a list into arbitrary indices, we need to create the nested lists with a conservative number of spots. We'll use the number of locales n and create what amounts to an nxn matrix--n lists with n terms each. Of course, this will be overly large, so we may thereafter need to remove items, for performance. But, actually, we're not using nested lists for performance.

# To find the number of locales, we need to know how many entries each locale has, and divide the length of newInitialList by that...and by two--one entry is two elements, the eventual key-value pair.

numAttr = 11 #The number of attributes each locale has.
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
                    finalList[i][j].append({"navigable" : "no", 'ijk': "%i %i %i" % (i, j, k),  'shortDesc' : hereBeList[k][i % (len(hereBeList) - 2) + 2].rstrip('\n').lstrip()})
            else:
                if not ignorePattern.search(hereBeList[2][k % (len(hereBeList) - 2) + 2]):
                    # Amending this to indicate the "hereBeMonsters" locales are off-limits. Will compare x attribute.
                    finalList[i][j].append({"navigable" : "no", 'ijk': "%i %i %i" % (i, j, k),  'shortDesc' : hereBeList[2][i % (len(hereBeList) - 2) + 2].rstrip('\n').lstrip()})


# for i in range(numLocales):
#     for j in range (numLocales):
#         # print "(%i, %i)" % (i, j),
#         print finalList[j][i]
# 
# wait = raw_input('Break now.')



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
                            intermeDict[newInitialList[n+20]]=newInitialList[n+21]
    
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

                            # Before we write the dict to the entry, we'll convert any #-delimited value string into a dict.
                            for m in intermeDict:
                                if re.search("#", intermeDict[m]):
                                    mDict = {}
                                    a = 0
                                    mList = re.split("#", intermeDict[m])
                                    if len(mList) % 2 != 0:
                                        print "Warning: The number of delimited elements in %s is uneven. This means there is a key without a value." % m
                                    while a < len(mList) - 1:
                                        mDict[mList[a]] = mList[a + 1]
                                        a += 2
                                    intermeDict[m] = mDict

                            # Now the full list is ready to write to the location.
                            finalList[k][j][i] = intermeDict 


# # This allows testing all locales.
# for i in range(numLocales):
#     for j in range (numLocales):
#         # print "(%i, %i)" % (i, j),
#         for k in range(numLocales):
#             print "%i, %i, %i:" % (k, j, i), finalList[k][j][i]
#             wait=raw_input("Dude there are a lot of these.")
# 
# print "The name of the item in (0, 0, 0) is %s." % finalList[0][0][0]["item_1"]["name"]

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


#####################CHARACTER#####################

# First, open the character attributes file.
charSource = open('character_Daniel', 'r')

initialCharList = []
for line in charSource:
    if not ignorePattern.search(line):
        initialCharList.append(re.split(':', line.rstrip('\n').lstrip()))

# print initialCharList
# boobs = raw_input("go")

charDict = {}
for item in initialCharList:
    charDict[item[0]] = item[1]
print charDict


boobs = raw_input("go")

























































####################/CHARACTER#####################


# initialPosition = [0,0,0]
# print finalList[initialPosition[0]][initialPosition[1]][initialPosition[2]]["longDesc"]
charDict["x"] = int(charDict["x"])
charDict["y"] = int(charDict["y"])
charDict["z"] = int(charDict["z"])
print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["longDesc"]
# position = initialPosition
# charDict["x"] = initialPosition[0]
# charDict["y"] = initialPosition[0]
# charDict["z"] = initialPosition[0]
directive = raw_input('What do you want to do? \n')
# print len(finalList)
# print len(finalList[0])
# directive = "QUIT"
while directive != "QUIT":
    # Need to parse 'directive' for directions
    if directive == "N":
        if charDict["y"] == 0:
            print "You can't go that way asshole."
        elif finalList[charDict["x"]][charDict["y"] - 1][charDict["z"]]["navigable"] == "no":
            print " %s \n You cannot go that way." % finalList[charDict["x"]][charDict["y"] - 1][charDict["z"]]["shortDesc"]
        else:
            charDict["y"] -= 1
            print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["longDesc"]
    elif directive == "S":
        if charDict["y"] == numLocales - 1:
            print "You can't go that way asshole."
        elif finalList[charDict["x"]][charDict["y"] + 1][charDict["z"]]["navigable"] == "no":
            print " %s \n You cannot go that way." % finalList[charDict["x"]][charDict["y"] + 1][charDict["z"]]["shortDesc"]
        else:
            charDict["y"] += 1
            print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["longDesc"]
    elif directive == "E":
        if charDict["x"] == numLocales - 1:
            print "You can't go that way asshole."
        elif finalList[charDict["x"] + 1][charDict["y"]][charDict["z"]]["navigable"] == "no":
            print " %s \n You cannot go that way." % finalList[charDict["x"] + 1][charDict["y"]][charDict["z"]]["shortDesc"]
        else:
            charDict["x"] += 1 
            print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["longDesc"]

            # Note that not every location will have "a large shelf" containing everything. You'll need to add a few additional
            # components as part of your locale attributes, e.g., "storage" = "A large shelf", etc. Some things might be on the floor,
            # some in the "storage" structure, and some...in *another* storage structure?
            itemString = ""
            for item in ("item_1","item_2","item_3","item_4","item_5"):
                if finalList[charDict["x"]][charDict["y"]][charDict["z"]][item] != "":
                    itemString += finalList[charDict["x"]][charDict["y"]][charDict["z"]][item]

            if itemString != "":
                print "A large shelf contains " + itemString + "."
    elif directive == "W":
        if charDict["x"] == 0:
            print "You can't go that way asshole."
        elif finalList[charDict["x"] - 1][charDict["y"]][charDict["z"]]["navigable"] == "no":
            print " %s \n You cannot go that way." % finalList[charDict["x"] - 1][charDict["y"]][charDict["z"]]["shortDesc"]
        else:
            charDict["x"] -= 1
            print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["longDesc"]
    elif directive == "U":
        if charDict["z"] == numLocales - 1: 
            print "You can't go that way asshole."
        elif finalList[charDict["x"]][charDict["y"]][charDict["z"] + 1]["navigable"] == "no":
            print " %s \n You cannot go that way." % finalList[charDict["x"]][charDict["y"]][charDict["z"] + 1]["shortDesc"]
        else:
            charDict["z"] += 1 
            print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["longDesc"]
    elif directive == "D":
        if charDict["z"] == 0:
            print "You can't go that way asshole."
        elif finalList[charDict["x"]][charDict["y"]][charDict["z"] - 1]["navigable"] == "no":
            print " %s \n You cannot go that way." % finalList[charDict["x"]][charDict["y"]][charDict["z"] - 1]["shortDesc"]
        else:
            charDict["z"] -= 1
            print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["longDesc"]
    elif directive == "I":
        print "You are currently carrying the following items:"
        for thing in ("item_1","item_2","item_3","item_4","item_5"):
            if charDict[thing] != "":
                print "    " + charDict[thing] 
    elif re.match("^GET", directive) is not None:
        directiveSplit = re.split(" ", directive) # Need to use this to parse the input for all possible values, not just the GET.
        # print directiveSplit
        # print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["item_1"]
        # print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["item_1"].upper()

        # Check to make sure the player has room for the item, and take note of the open slot.
        invCount = 0
        openItem = []
        for item in ("item_1","item_2","item_3","item_4","item_5"):
            if charDict[item] != "":
                # print charDict[item]
                invCount += 1
            else:
                openItem.append(item)
                
        if invCount == 5:
            print "You have no room for that."
        else:
            for item in ("item_1","item_2","item_3","item_4","item_5"):
                if re.match(directiveSplit[1].upper(), \
                        finalList[charDict["x"]][charDict["y"]][charDict["z"]][item].upper()):
                    charDict[openItem[0]] = \
                        finalList[charDict["x"]][charDict["y"]][charDict["z"]][item]
                    finalList[charDict["x"]][charDict["y"]][charDict["z"]][item] = "" # Need loop to check if there *are* any items before displaying list.
                    print "You picked up %s." % charDict[openItem[0]]
    elif re.match("^DROP", directive) is not None:
        directiveSplit = re.split(" ", directive)
        # First let's make sure we're dropping something we're carrying.
        itemLocation = []
        openLocation = []
        openSlots = 0
        for item in ("item_1","item_2","item_3","item_4","item_5"):
            if re.match(directiveSplit[1].upper(),charDict[item].upper()):
                itemLocation.append(item) # There may be multiple matches, so we'll keep 'em all.

        if len(itemLocation) == 0:
            "You aren't carrying any %s." % directiveSplit[1]
        else:
            for item in ("item_1","item_2","item_3","item_4","item_5"):
                if finalList[charDict["x"]][charDict["y"]][charDict["z"]][item] == "":
                    openLocation.append(item) 

            # If there are open slots, DROP the item, else say there's no room.
            if len(openLocation) > 0:
                finalList[charDict["x"]][charDict["y"]][charDict["z"]][openLocation[0]] = charDict[itemLocation[0]] # DROP the first matched inventory item into the first open slot.
                charDict[itemLocation[0]] = ""
                print "You have dropped your %s." % finalList[charDict["x"]][charDict["y"]][charDict["z"]][openLocation[0]]
            else:
                print "There is no room for that here."
    elif re.match("^LOOK", directive) is not None:
        directiveSplit = re.split(" ", directive)
        print finalList[charDict["x"]][charDict["y"]][charDict["z"]]["longDesc"]
        # Note that not every location will have "a large shelf" containing everything. You'll need to add a few additional
        # components as part of your locale attributes, e.g., "storage" = "A large shelf", etc. Some things might be on the floor,
        # some in the "storage" structure, and some...in *another* storage structure?
        itemString = ""
        for item in ("item_1","item_2","item_3","item_4","item_5"):
            if finalList[charDict["x"]][charDict["y"]][charDict["z"]][item] != "":
                itemString += finalList[charDict["x"]][charDict["y"]][charDict["z"]][item]

        if itemString != "":
            print "A large shelf contains " + itemString + "." # This belongs in the locale, and each object should have its place in the locale.

    # else:
        # Something like "I don't understand." This is the else clause for the whole interaction loop.
                    
    directive = raw_input('What do you want to do ? \n')



###################FILE SAVE###################
print "Saving progress..."

########### to do ######################################################
# Need to create a list of attribute keys, and iterate over that list,
# instead of iterating over keys in the locale. This will make the
# save file structure like our initialization file, so we can
#   a. read the file easily;
#   b. reuse the same game loading code; and
#   c. probably something else cool.
########################################################################
# First, open the locale attributes file.
localeSourceAgain = open('localeAttributes.txt', 'r')
i = 0
attrKeyListInit = []
attrKeyListFin = []
for line in localeSourceAgain:
    if not ignorePattern.search(line):
        attrKeyListInit.append(re.split(':', line))
        i += 1
        if i == numAttr:
            break
print "Here is attrKeyListInit."
print attrKeyListInit
for attrList in attrKeyListInit:
    attrKeyListFin.append(attrList[0])
print "Here is attrKeyListFin."
print attrKeyListFin
print "Here is finalList 0 0 0"
print finalList[0][0][0]
print "Here is finalList 0 0 0 x"
print finalList[0][0][0]['x']

############ notes ##########################################################
# So the deal is, the hereBeMonsters areas don't have an "x" attribute, which
# breaks our save template below. Need to make hereBeMon areas compatible.
############ /notes #########################################################

saveList = []
for i in range(numLocales):
    for j in range (numLocales):
        # print "(%i, %i)" % (i, j),
        for k in range(numLocales):
            # for key in finalList[k][j][i]:
            for key in attrKeyListFin:
                print "Here is finalList %i %i %i" % (k, j, i)
                print finalList[k][j][i]
                print "Here is finalList %i %i %i %s" % (k, j, i, key)
                print finalList[k][j][i][key]
                d00d = raw_input('THIS SHIT IS REAL DAWG')
                if isinstance(finalList[k][j][i][key], str):
                    saveStr = "%s: %s" % (key, finalList[k][j][i][key])
                    saveList.append(saveStr)
                    # print saveStr
                    # d00d = raw_input('THIS SHIT IS REAL DAWG')
                elif isinstance(finalList[k][j][i][key], dict):
                    attrStr = ""
                    for key2 in finalList[k][j][i][key]:
                        attrStr = attrStr + "%s#%s#" % (key2, finalList[k][j][i][key][key2])
                    # Strip the trailing octothorpe
                    attrStr = attrStr[:len(attrStr) - 1]
                    saveStr = "%s: %s" % (key, attrStr)
                    saveList.append(saveStr)
                    # print saveStr
                    # d00d = raw_input('THIS SHIT IS REAL DAWG')
# 
# 
# # Ask user for save filename of choice.
# saveFileName = raw_input('Save game filename: ')
# # Now we write the save file.
# saveFile = open(saveFileName, 'w')
# saveFile.write('\n'.join(saveList))
# saveFile.close




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
