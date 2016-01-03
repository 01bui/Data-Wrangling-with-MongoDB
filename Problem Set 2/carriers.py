#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI
# All your changes should be in the 'extract_carrier' function
# Also note that the html file is a stripped down version of what is actually on the website.

# Your task in this exercise is to get a list of all airlines. Exclude all of the combination
# values, like "All U.S. Carriers" from the data that you return.
# You should return a list of codes for the carriers.

from bs4 import BeautifulSoup
import requests
html_page = "options.html"


def extract_carriers(page):
    data = []

    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")

        #eventvalidation = soup.find(id="__EVENTVALIDATION")
        #data['eventvalidation'] = eventvalidation.get('value')

        #viewstate = soup.find(id="__VIEWSTATE")
        #data['viewstate'] = viewstate.get('value')

        airportList = []
        for item in soup.find_all('select',id="AirportList"):
            for i in item.find_all('option'):
                if len(i.get('value')) == 3:
                    airportList.append(i.get('value'))
        #print airportList[2:]
        #data['airport'] = airportList[1:]

        carrierList = []
        for item in soup.find_all('select',id="CarrierList"):
            for i in item.find_all('option'):
                carrierList.append(i.get('value'))
        data = carrierList[3:]
    #print data
    #print len(data)
    return data


def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]
    airport = data["airport"]
    carrier = data["carrier"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': airport,
                          'CarrierList': carrier,
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


def test():
    data = extract_carriers(html_page)
    assert len(data) == 16
    assert "FL" in data
    assert "NK" in data

test()