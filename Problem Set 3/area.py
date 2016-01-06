#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.

Since in the previous quiz you made a decision on which value to keep for the "areaLand" field,
you now know what has to be done.

Finish the function fix_area(). It will receive a string as an input, and it has to return a float
representing the value of the area or None.
You have to change the function fix_area. You can use extra functions if you like, but changes to process_file
will not be taken into account.
The rest of the code is just an example on how this function can be used.
"""
import codecs
import csv
import json
import pprint
from decimal import *

CITIES = 'cities.csv'


def fix_area(area):

    # YOUR CODE HERE

    # YOUR CODE HERE
    try:
        thisNum = float(area)
        decimalPoint = thisNum - int(thisNum)
        if decimalPoint == 0:
            int(area)
    except ValueError:
        if (area == "NULL") or (area == ""):
            area = None
        elif area.startswith("{"):
            values = area[1:-1].split("|")
            value1Count = int(values[1].split("+")[1])
            value0Count = int(values[0].split("+")[1])

            value1C = (values[1].split("e")[0])
            value0C = (values[0].split("e")[0])

            print values, value0Count, value1Count, value0C, value1C
            if len(value1C) > len(value0C) and value1Count > value0Count:
                area = float(values[1])
                #print values, area
            if len(value0C) > len(value1C) and value1Count < value0Count:
                area = float(values[0])
            if value1Count == value0Count:
                print values
                if len(value0C) > len(value1C):
                    area = float(values[0])
                else:
                    area = float(values[1])

    return area



def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        #skipping the extra metadata
        for i in range(3):
            l = reader.next()

        # processing file
        for line in reader:
            # calling your function to fix the area value
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print "Printing three example results:"
    for n in range(5,8):
        pprint.pprint(data[n]["areaLand"])

    print data[8]["areaLand"]
    print data[20]["areaLand"]
    print data[33]["areaLand"]


    assert data[3]["areaLand"] == None
    assert data[8]["areaLand"] == 55166700.0
    assert data[20]["areaLand"] == 14581600.0
    assert data[33]["areaLand"] == 20564500.0


if __name__ == "__main__":
    test()