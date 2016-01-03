def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        ev = soup.find(id="__EVENTVALIDATION")
        data["eventvalidation"] = ev["value"]

        vs = soup.find(id="__VIEWSTATE")
        data["viewstate"] = vs["value"]

    return data

#Note that the second argument to the BeautifulSoup function, "lxml",
#  comes from the parser in the Python library 'lxml'.
#Other parsers can be set up as the second argument, such as the Python library's default "html.parser" or
    # other options as shown in the documentation.
    # Take note of this argument when working with BeautifulSoup on your local computer.