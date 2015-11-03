__author__ = 'Ryan Schulman'
import urllib.request
import sys
from lxml import html
import requests
import string
from bs4 import BeautifulSoup, Comment
import urllib
from enchant.checker import SpellChecker
from enchant import Dict
import re
#global finished_links
#finished_links = []


class TNode(object):  # Nodes of the tree. 1 parent, unlimited children via list
    def __init__(self, page, parent, children=[]):
        self.page = page
        self.parent = parent
        self.children = children

    def hasChild(self):
        if len(self.children) != 0:
            return True
        else:
            return False


class Page(object):  # when passed is true, the page has a 200 code. Otherwise it fails
    text = "Not yet set"

    def __init__(self, url, passed, domain):
        self.url = url
        self.passed = passed
        self.domain = domain

    def setText(self, text):
        self.text = text

    def isOnDomain(self):
        if (self.url.find(self.domain) == -1):  #and self.url.find("radio.uccs.edu") == -1):#need to add all sll domains/sub-domains
            return False
        else:
            return True


# tkaes a string
def testUrl(link):  #test url for non 200 message
    try:
        opener = urllib.request.urlopen(link)
        site = opener.read()
        code = opener.getcode()

        if (code // 100 == 2):  #any code that starts with a 2
            return True
        else:
            return False
    except:
        return False


#takes a string and a node
def makePage(temp, parent, domain):
    link = temp
    try:
        opener = urllib.request.urlopen(link)
        code = opener.getcode()
    except:
        return TNode(Page(link, False), parent, {None})

    if (code == 200):
        #
        url = requests.get(link)
        tree = html.fromstring(url.text)
        page = Page(link, True, domain)
        current = TNode(page, parent, children=[])
        pageHasURLs = False
        #urlText = tree.xpath('//a/text()')
        urls = tree.xpath('//a/@href')
        urlText = tree.xpath('//a')
        for x, y in zip(urls, urlText):  #for all the links in a page
            if (len(y.xpath('text()')) > 0):
                text = y.xpath('text()')[0]
                #print("url: "+x+"text: "+y.xpath('text()')[0])
            else:
                text = "none, may be an image"
                #print("url: "+x+"text: none, may be an image")
            pageHasURLs = True

            if (x.find(
                    "mailto") != -1):  #mailto links are ignored, remove continue and comment marks to mark them as failed instead
                continue
                #newPage = Page(x, False)
                #current.children.append(TNode(newPage, current, None))

            elif (x.find(".com") != -1 or x.find(".org") != -1 or x.find(".net") != -1 or x.find(
                    ".edu") != -1 or x.find(".gov") != -1
                  or x.find(".info") != -1 and x.find(
                        "club_find") == -1):  #if it's a link, and it's not under "find a club"

                if (x.find("http:") == -1 and x.find("https:") == -1):  #make sure url has http
                    x = "http:" + x

                test = testUrl(x)
                newPage = Page(x, test, domain)
                newPage.setText(text)
                current.children.append(TNode(newPage, current, None))

        if (
        not pageHasURLs):  #tests for 404 pages that don't return a 404 error message. Will break if urls are added to 404 pages.
            current.page.passed = False

        return current
    else:
        return TNode(Page(link, False, domain), parent, None)


#algorithm for make site function
#while link is on uccs domain
#if page.passed is true
#make page
#move onto children

#takes a URL
def makeSite(link, domain):  #make the website into a tree of urls
   # print("######################")
    #print("page: " + link)

    root = makePage(link, None, domain)
    finished_links=[link]
    makeSiteHelper(root, domain, finished_links)
    return root


def makeSiteHelper(current, domain, finished_links):  #takes a node
    if current.page.isOnDomain():
        if (current.children is not None):
            i = 0
            for x in current.children:
                if (x.page.isOnDomain() and x.page.url not in finished_links and x.page.passed):
                    finished_links.append(x.page.url)  #keeps track of links we have looked at
                    print("page: " + x.page.url)
                    tempPage = makePage(x.page.url, current, domain)  #make page from child page
                    tempPage.page.setText(x.page.text)
                    current.children.insert(i, tempPage)  #insert new page into location that once had child page
                    current.children.remove(x)  #remove old child page
                    makeSiteHelper(tempPage, domain, finished_links)  #move onto that child's children
                    i = 1 + i  #incrment list index


def printTree(root):  #takes a node
    printTreeHelper(root)


def printTreeHelper(current):  #takes a node
    if current is not None:
       # print("%50s%-s", current.page.url, current.page.passed)
        if current.children is not None:
            for x in current.children:
                printTreeHelper(x)


global failed_links_messages
failed_links_messages = []

def printTree(root):
    printTreeHelper(root)
def printTreeHelper(current):
    print(current.page.url)
    if current.children is not None:
        print("\n-------Branch---------")
        for x in current.children:
            print(x.page.url)
        for x in current.children:
            printTreeHelper(x)

def validate(root):  #takes a node
    validateHelper(root)


def validateHelper(current):  #takes a node
    if (current.children is not None):
        for x in current.children:
            if x.page.passed:
                validateHelper(x)
            else:
                message = x.parent.page.url + " this page failed to load URL: " + x.page.url + " Link: " + x.page.text
                failed_links_messages.append(message)
                #print(message)
#found this at http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('.*<!--.*-->.*', string, re.DOTALL):
        return False
    return True
def spellcheck(root):
    finished_links = []
    spellcheckhelper(root, finished_links)
def spellcheckhelper(current, finished_links):
    if current.page.passed and current.page.url not in finished_links:
        finished_links.append(current.page.url)
        response = urllib.request.urlopen(link)
        html =response.read()
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.body
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()

        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('img')]
        [s.extract() for s in soup('a')]
        texts = soup.findAll(text=True)
        checker= SpellChecker('en_US')
        checker.set_text(''.join(texts))
        errors = []#to be filled with strings
        for err in checker:
            if any(s in err.word for s in string.ascii_uppercase):
                pass
            else:
                errors.append(err.word)

        if errors is not None:
            print("----------------\n"+current.page.url)
        for word in errors:
            dictionary = Dict()
            print ("ERROR: " + word + "\nOur best guesses: ")
            [print(w) for w in dictionary.suggest(str(word))]
            print("----")

        print("------")
        if(current.children is not None):
            for x in current.children:
                spellcheckhelper(x, finished_links)


def run(link, domain):
    print("Building site: ")
    root = makeSite(link, domain)
    print("Site built")
    return root

#array of sites you want scanned. probably a bit redundant
link = "http://sll.uccs.edu/"
domain = "sll.uccs.edu/"
root = run(link, domain)
spellcheck(root)