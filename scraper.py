import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup


# TODO: later, record ans to all 4 questions

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def defragment(URL):
    return URL.split('#')[0] if '#' in URL else URL


def extract_next_links(url, resp):
    # TODO: only allow page with high text information contents (check piazza @125)
    # TODO: (question answering)
    #      1. unique URLs  (discard fragment!) # Done
    #      2. longest page in terms of the number of words?        beautifulsoup parse 'rawdata'.content  strip string  --> text representation of page
    #      3. 50 most common words (Ignore English stop words!) -> Submit the list of common words ordered by frequency.
    #      4. How many subdomains in the ics.uci.edu domain?

    try:  # filter out page with no data
        data = resp.raw_response.content  # can use .content (contents in bytes) or .text
    except:
        return []

    data = resp.raw_response.content  # can use .content (contents in bytes) or .text
    soup = BeautifulSoup(data, 'html.parser')

    result = []
    # Extract all <a> tags, get its 'href' value
    for link in soup.find_all('a'):
        result.append(link.get('href'))
    return result


def is_valid(url):
    # TODO: 1. filter out infinite traps
    #       2. filter out sets of similar pages
    #       3. avoid crawling very large file

    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False

        # restrict to only 5 allowed domains
        DOMAIN_LIST = [
            '.ics.uci.edu',
            '.cs.uci.edu',
            '.informatics.uci.edu',
            'today.uci.edu/department/information_computer_sciences'
        ]

        for domain in DOMAIN_LIST:
            if domain in parsed.hostname:
                hostname_valid = True
                break
            else:
                hostname_valid = False

        if parsed.hostname is None or not hostname_valid:
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
