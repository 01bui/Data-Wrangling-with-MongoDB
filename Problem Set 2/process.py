#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Let's assume that you combined the code from the previous 2 exercises
# with code from the lesson on how to build requests, and downloaded all the data locally.
# The files are in a directory "data", named after the carrier and airport:
# "{}-{}.html".format(carrier, airport), for example "FL-ATL.html".
# The table with flight info has a table class="dataTDRight".
# There are couple of helper functions to deal with the data files.
# Please do not change them for grading purposes.
# All your changes should be in the 'process_file' function
# This is example of the datastructure you should return
# Each item in the list should be a dictionary containing all the relevant data
# Note - year, month, and the flight data should be integers
# You should skip the rows that contain the TOTAL data for a year
# data = [{"courier": "FL",
#         "airport": "ATL",
#         "year": 2012,
#         "month": 12,
#         "flights": {"domestic": 100,
#                     "international": 100}
#         },
#         {"courier": "..."}
# ]
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"


def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
    return files


def process_file(f):
    """This is example of the data structure you should return.
    Each item in the list should be a dictionary containing all the relevant data
    from each row in each file. Note - year, month, and the flight data should be
    integers. You should skip the rows that contain the TOTAL data for a year
    data = [{"courier": "FL",
            "airport": "ATL",
            "year": 2012,
            "month": 12,
            "flights": {"domestic": 100,
                        "international": 100}
            },
            {"courier": "..."}
    ]
    """
    data = []
    info = {}

    info["courier"], info["airport"] = f[:6].split("-")
    #print info
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list
    # will be a reference to the same info dictionary.
    with open("{}/{}".format(datadir, f), "r") as html:
        values = []
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('table',id="DataGrid1"):
            for j in item.find_all('tr'):
                #print j
                for i in j.find_all('td'):
                    #print i
                    for string in i.strings:
                        values.append(string)

        #print values[5:]
        values = values[5:]

        for i in range(0, len(values), 5):
            info = {}
            flights = {}
            #print values[i], values[i+1], values[i+2], values[i+3]
            if values[1+i] != "TOTAL":
                info["courier"], info["airport"] = f[:6].split("-")
                info["year"] = int(values[0+i])
                info["month"] = int(values[1+i])
                flights["domestic"] = int(values[2+i].replace(',', ''))
                flights["international"] = int(values[3+i].replace(',', ''))
                info["flights"] = flights
                #print info
                data.append(info)
            #print info
    #print len(data)


    return data


def test():
    print "Running a simple test..."
    open_zip(datadir)
    print
    files = process_all(datadir)
    data = []
    #print files
    for f in files:
        #print f
        data += process_file(f)
        #print process_file(f)
    #print len(data)
    assert len(data) == 399  # Total number of rows
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[0]["courier"] == 'FL'
    assert data[0]["month"] == 10
    assert data[-1]["airport"] == "ATL"
    assert data[-1]["flights"] == {'international': 108289, 'domestic': 701425}

    print "... success!"

if __name__ == "__main__":
    test()