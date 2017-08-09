#!/usr/bin/env python

import re
import json
import argparse

# parse a list of files
def parse(names):
    base = {}
    p = re.compile("^// (.*?)\:(.*)")

    for fname in names:
        modeldoc = open(fname, "r")
        tooltip = None

        for line in modeldoc:
            s = p.search(line)
            if s:
                obj = base
                keystr = s.group(1)     # // address.queue.label
                value = s.group(2)      # :the text after the first :

                keys = keystr.split('.')
                for i, key in enumerate(keys):
                    # the first keys define the object heirarchy
                    if i < len(keys) - 1:
                        if not key in obj:
                            obj[key] = {}
                        obj = obj[key]
                    # the last key gets the value
                    else:
                        # :start and :stop lines surround block values
                        if value == 'start':
                            tooltip = []                    # start accumulating tooltip lines
                            continue
                        elif value == 'stop':
                            obj[key] = ' '.join(tooltip)    # join the tooltip lines in to one line
                            tooltip = None
                            continue

                        # assign the value to the last key
                        obj[key] = value

            # are we accumulating tooltip lines
            elif tooltip is not None:
                tooltip.append(line.rstrip())

        modeldoc.close()

    return json.dumps(base, sort_keys=True, indent=4, separators=(',', ': '))


parser = argparse.ArgumentParser(description='Output json file made from Extracting comments from one or more asciidoc files.')
parser.add_argument('fnames', metavar='f', type=str, nargs='+',
                    help='Name[s] of the input asciidoc file[s]')
args = parser.parse_args()

print parse(args.fnames)