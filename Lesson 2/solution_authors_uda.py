def get_author(root):
    authors = []
    for author in root.findall('./fm/bibl/aug/au'):
        data = {
                "fnm": None,
                "snm": None,
                "email": None
        }
        data["fnm"] = author.find('./fnm').text
        data["snm"] = author.find('./snm').text
        data["email"] = author.find('./email').text

        authors.append(data)

    return authors