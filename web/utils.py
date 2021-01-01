import requests

def is_hyperlink(location):
    """Figuring out if a string is a hyperlink is surprisingly difficult, so just make a request and see.
       Or so you'd think! This works fine in Azure, but at home, I get a page from ISP about an unknown address
       and THAT page returns a 200. Watch out for this.
    """
    try:
        return requests.get(location).ok
    except requests.exceptions.MissingSchema:
        try:
            return requests.get('http://' + location).ok
        except requests.exceptions.ConnectionError:
            return False
    except requests.exceptions.ConnectionError:
        return False
