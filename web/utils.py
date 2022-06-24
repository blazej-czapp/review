import requests

def conversion_to_hyperlink(location):
    """Figuring out if a string is a hyperlink is surprisingly difficult, so just make a request and see.
       Or so you'd think! This works fine in Azure, but at home, I get a page from ISP about an unknown address
       and THAT page returns a 200. Watch out for this.

       Return a function that converts location to a valid hyperlink or None if not possible. Note that without
       a schema, a link is interpreted as relative to the page itself.
    """
    try:
        if requests.get(location).ok:
            return lambda loc: loc
    except requests.exceptions.MissingSchema:
        try:
            if requests.get('http://' + location).ok:
                return lambda loc: f'http://{loc}'
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
            return None
    except requests.exceptions.ConnectionError:
        return None
