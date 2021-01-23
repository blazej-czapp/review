import requests

def conversion_to_hyperlink(location):
    """Figuring out if a string is a hyperlink is surprisingly difficult, so just make a request and see.
       Or so you'd think! This works fine in Azure, but at home, I get a page from ISP about an unknown address
       and THAT page returns a 200. Watch out for this.

       Return a string to prepend to make location a proper hyperlink or None if not possible. Without the conversion
       (i.e. prepending a "http://"" if missing) a link would be interpreted as relative to the review page.
    """
    try:
        if requests.get(location).ok:
            return ''
    except requests.exceptions.MissingSchema:
        try:
            if requests.get('http://' + location).ok:
                return 'http://'
        except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
            return None
    except requests.exceptions.ConnectionError:
        return None
