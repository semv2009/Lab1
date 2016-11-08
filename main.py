import requests
import re
from urllib.parse import urlsplit
from lxml.html import fromstring

URL = 'http://www.mosigra.ru/'

def getHtml(url):
    parts = urlsplit(url)
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    if path[:4] != 'http':
        path = URL + path
    html = requests.get(path).content
    return html

def getLinks(html):
    links = [x.get('href') for x in fromstring(html).cssselect('a')[0:12]]
    return links

def getEmails(html):
    regular = re.compile(b"\w+\@\w+\.\w+")
    emails = set(reg for reg in regular.findall(html))
    return emails

def discoverEmails():
    direction = {}
    links = getLinks(getHtml(URL))
    for link in links:
        emails = getEmails(getHtml(link))
        for email in emails:
            direction[email] = ""
    return direction

if __name__ == '__main__':
    uniqEmails = discoverEmails()
    with open('output.txt', 'w') as f:
        for email in uniqEmails.keys():
            f.write(email.decode('utf-8') + '\n')