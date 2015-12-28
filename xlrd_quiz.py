#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min, max and average values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()

def avgerage(list):
    sum = 0
    for e in list:
        sum += e
    avg = sum/len(list)*1.0
    return avg;


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    # Read Excel file
    sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

    # Find and return the min, max and average values for the COAST region
    coast = [item[1] for item in sheet_data][1:]
    print type(coast[0])
    avg = avgerage(coast)
    print "Average Coast:"
    print avg
    minCoast = min(coast)
    maxCoast =  max(coast)
    print "Min Coast:"
    print minCoast
    print "Max Coast:"
    print maxCoast

    # Find and return the time value for the min and max entries
    # The time values should be returned as Python tuples
    # Another way is to use list.index(value) + 1 to locate the index of min and max values
    minCoastIndex = 0
    maxCoastIndex = 0
    for item in coast:
        minCoastIndex += 1
        if item == minCoast:
            break
    for item in coast:
        maxCoastIndex += 1
        if item == maxCoast:
            break
    print "minCoastIndex and maxCoastIndex:"
    print minCoastIndex
    print maxCoastIndex

    time  = sheet.col_values(0, start_rowx=1, end_rowx=None)
    print "Time value for the min and max entries:"
    minTime = sheet.cell_value(minCoastIndex, 0)
    print xlrd.xldate_as_tuple(minTime, 0)
    maxTime = sheet.cell_value(maxCoastIndex, 0)
    print xlrd.xldate_as_tuple(maxTime, 0)

    ### example on how you can get the data
    #sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

    ### other useful methods:
    # print "\nROWS, COLUMNS, and CELLS:"
    # print "Number of rows in the sheet:",
    # print sheet.nrows
    # print "Type of data in cell (row 3, col 2):",
    # print sheet.cell_type(3, 2)
    # print "Value in cell (row 3, col 2):",
    # print sheet.cell_value(3, 2)
    # print "Get a slice of values in column 3, from rows 1-3:"
    # print sheet.col_values(3, start_rowx=1, end_rowx=4)

    # print "\nDATES:"
    # print "Type of data in cell (row 1, col 0):",
    # print sheet.cell_type(1, 0)
    # exceltime = sheet.cell_value(1, 0)
    # print "Time in Excel format:",
    # print exceltime
    # print "Convert time to a Python datetime tuple, from the Excel float:",
    # print xlrd.xldate_as_tuple(exceltime, 0)


    data = {
            'maxtime': (0, 0, 0, 0, 0, 0),
            'maxvalue': 0,
            'mintime': (0, 0, 0, 0, 0, 0),
            'minvalue': 0,
            'avgcoast': 0
    }

    data['maxtime'] = xlrd.xldate_as_tuple(maxTime, 0)
    data['mintime'] = xlrd.xldate_as_tuple(minTime, 0)
    data['maxvalue'] = maxCoast
    data['minvalue'] = minCoast
    data['avgcoast'] = avg

    print data

    return data


def test():
    #open_zip(datafile)
    data = parse_file(datafile)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)


test()