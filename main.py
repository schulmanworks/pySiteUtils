__author__ = 'rschulma'
import urllib.request
import re
from lxml import html
import requests

class TNode(object):
    def __init__(self, page, parent, children = []):
        self.page = page
        self.parent = parent
        self.children = children



class Page(object):
    def __init__(self,url, passed):
        self.url = url
        self.passed = passed

def testUrl(link):
    opener = urllib.request.urlopen(link)
    code = opener.getcode()
    if(code == 200):
        return True
    else:
        return False

def makePage(temp):
    link = temp
    opener = urllib.request.urlopen(link)
    code = opener.getcode()
    print(code)
    if(code == 200):
        print("working")
        url = requests.get(link)
        tree = html.fromstring(url.text)
        page = Page(link, True)
        current = TNode(page, None, None)
        children = []
        for x in tree.xpath('//a/@href'):
            if(x.find("mailto")!=-1):
                newPage = Page(url, False)
                children.append(TNode(newPage, current, None))
                print(x)
            else:
                if(x.find("http:")==-1 and x.find("https:")==-1):
                    url = "http:"+x
                else:
                    url = x
                print(url)
                test = testUrl(url)
                newPage = Page(url, test)
                children.append(TNode(newPage, current, None))
                current.children = children
    return current

link = 'http://sll.uccs.edu/'
root = makePage(link)
