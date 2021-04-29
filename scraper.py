import re
import string
from collections import defaultdict
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from crawler import frontier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from urllib.parse import urljoin
from urllib.parse import urldefrag

# 1. record pages that are crawled (did in frontier)
# 2. record longest page in terms of the number of words
longest_page_url = ""
longest_page_word_count = 0
# 3. most common words
words_freq = defaultdict(int)
# 4. how many subdomains
visited_subdomains = dict()


def scraper(url, resp):
    links = extract_next_links(url, resp)

    # record 4 questions into file
    with open("my_record.txt", "w", encoding="utf-8") as file:
        file.write("Longest Page URL:" + longest_page_url + "\n")
        file.write("Longest Page URL Length:" + str(longest_page_word_count) + "\n")
        file.write("Most common words:" + str(words_freq) + "\n")
        file.write("Visited Domain:" + str(visited_subdomains) + "\n")
    file.close()

    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # TODO: only allow page with high text information contents (check piazza @125)
    global longest_page_url, longest_page_word_count, words_freq, visited_subdomains

    # filter out invalid page or page with no data
    if resp.status != 200 or resp.raw_response.content is None:
        return []

    data = resp.raw_response.content
    soup = BeautifulSoup(data, 'html.parser')

    # find longest page, the following code comes from https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    text = ' '.join(soup.stripped_strings)
    stop_words = set(stopwords.words('english'))
    text_tokens = word_tokenize(text)
    filtered_text = []

    # record most common words
    for w in text_tokens:
        if w not in stop_words and w not in string.punctuation:
            words_freq[w] += 1
            filtered_text.append(w)

    if len(filtered_text) > longest_page_word_count:
        longest_page_url = url
        longest_page_word_count = len(filtered_text)

    # record subdomain
    subdomain = urlparse(url).hostname
    if subdomain not in visited_subdomains:
        visited_subdomains[subdomain] = 1
    else:
        visited_subdomains[subdomain] += 1

    result_links = []
    # Extract all <a> tags, get its 'href' value
    for link in soup.find_all('a'):
        link = urljoin(url, link.get('href'))
        link = urldefrag(link)[0]  # defragment the url
        result_links.append(link)
    return result_links


def is_valid(url):
    # TODO: 1. filter out sets of similar pages
    #       2. avoid low information value

    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False

        if parsed.hostname is None:
            return False

        # filter out traps
        avoid_crawling = ["#", "?", "%", "+", "&", "@", "calendar", "files", "pdf", "txt", "jpg",
                          "war", "apk", "img", "sql", "bib", "pps", "photo", "attachment", ".odc",
                          "wics.ics.uci.edu/events/", "www.ics.uci.edu/ugrad/honors/index.php/",
                          "ds_store", "www.ics.uci.edu/honors/", "balluru.thesis", "/uploads/",
                          ".py", "largefam3-haplo", "~dechter/r", ".bam", "archive.ics.uci.edu/ml/00"]
        for a in avoid_crawling:
            if a in url.lower():
                return False

        # filter out repeated path name
        path = parsed.path.lower()
        path_list = list(filter(lambda p: p != '', path.split('/')))   # avoid "//" in path
        if len(set(path_list)) != len(path_list):
            return False

        # restrict to only 5 allowed domains
        hostname = parsed.hostname
        if not ('.ics.uci.edu' in hostname or
                '.cs.uci.edu' in hostname or
                '.informatics.uci.edu' in hostname or
                '.stat.uci.edu' in hostname or
                'today.uci.edu/department/information_computer_sciences' in hostname):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|ppsx)$", parsed.path.lower())  # added ppsx

    except TypeError:
        print("TypeError for ", parsed)
        raise
