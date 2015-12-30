# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = None
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    # Read Excel file
    sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]
    time  = sheet.col_values(0, start_rowx=1, end_rowx=None)
    # Find the time and value of max load for each of the regions
    # COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
    temp_data = []
    value = []
    data = {}
    key = ['Year', 'Month', 'Day', 'Hour', 'Max Load']
    for i in range(1,9):
        value = []
        field = [item[i] for item in sheet_data][1:]
        maxVal = max(field)
        #maxIdx = field.index(maxVal) + 1
        maxIdx = 0
        for item in field:
            maxIdx += 1
            if item == maxVal:
                break
        maxTime = sheet.cell_value(maxIdx, 0)
        maxTimeTuple = xlrd.xldate_as_tuple(maxTime, 0)
        value = list(maxTimeTuple[:4]) # eliminate minute and second
        print maxVal, value, maxIdx
        value.append(maxVal)
        temp_data.append(zip(key, value))
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH', 'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']

    i = 0
    for item in temp_data:
        #print item
        data.update({correct_stations[i]: dict(item)})
        i += 1
    #print temp_data
    #print data
    return data


def save_file(data, filename):
    # YOUR CODE HERE
    # Station|Year|Month|Day|Hour|Max Load
    with open(filename, 'w') as csvfile:
        fieldnames = ['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="|")

        writer.writeheader()
        keys = data.keys()
        values = data.values()
        for i in range(len(data)):
            writer.writerow({'Station': keys[i], 'Year': values[i]['Year'], 'Month': values[i]['Month'], 'Day': values[i]['Day'], 'Hour': values[i]['Hour'], 'Max Load':values[i]['Max Load']})



def test():
    #open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        #print max_answer, max_line
                        assert max_answer == max_line
                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()
