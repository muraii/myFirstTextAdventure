#!/usr/bin/env python
import re

# First, open the locale attributes file.
localeSource = open('localeattributes.py','r')

# Now populate the list of lists of dicts with locale data.
# First, compile the search pattern for comments and empty lines.
ignorePattern = re.compile('^#\w.|^\n')

for line in localeSource:
    if ignorePattern.search(line):
        # some code that parses crap or whatever, returning a list of
        # dictionaries, e.g., [{'x': 0, 'y': 0, 'desc': '...'},...]
        localAttributeList = [
