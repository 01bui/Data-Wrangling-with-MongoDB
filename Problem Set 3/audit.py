#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a
SET of the types that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values
first.
"""
import codecs
import csv
import json
import pprint
import pdb

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal",
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long",
          "areaLand", "areaMetro", "areaUrban"]

def audit_file(filename, fields):
    fieldtypes = {}
    for field in FIELDS:
        fieldtypes.update({field: set()})

    # YOUR CODE HERE
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        reader.next()
        reader.next()
        reader.next() # Skip the first three lines
        for row in reader:
            #print row
            for field in FIELDS:
                #pdb.set_trace()
                #print row[field]

                try:
                    thisNum = float(row[field])
                    decimalPoint = thisNum - int(thisNum)
                    if decimalPoint == 0:
                        thisType = type(1) #int
                    thisType = type(1.1) #float
                    fieldtypes[field].add(thisType)
                except ValueError:
                    if (row[field] == "NULL") or (row[field] == ""):
                        fieldtypes[field].add(type(None))
                    elif row[field].startswith("{"):
                        fieldtypes[field].add(type([]))
                    else:
                        thisType = type(row[field]) #str type
                        fieldtypes[field].add(thisType)

    #print fieldtypes
    return fieldtypes


def test():
    print set([type(1.1), type([]), type(None)])
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])

if __name__ == "__main__":
    test()
