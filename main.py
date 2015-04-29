__author__ = 'rschulma'
import urllib.request
import re
from lxml import html
import requests
finished_links = []
class TNode(object):
    def __init__(self, page, parent, children = []):
        self.page = page
        self.parent = parent
        self.children = children
    def hasChild(self):
        if len(self.children) != 0:
            return True
        else: return False




class Page(object):
    def __init__(self,url, passed):
        self.url = url
        self.passed = passed
    def isOnDomain(self):
        if(self.url.find("sll.uccs.edu") == -1 and self.url.find("radio.uccs.edu") == -1):#need to add all sll domains/sub-domains
            return False
        else:
            return True

def testUrl(link):
    try:
        opener = urllib.request.urlopen(link)
        code = opener.getcode()
        if(code == 200):
            return True
        else:
            return False
    except:
        return False

def makePage(temp, parent):
    print("loading")
    link = temp
    try:
        opener = urllib.request.urlopen(link)
        code = opener.getcode()
    except:
        return TNode(Page(link, False),parent,None)
    #print(code)
    if(code == 200):
       #
        url = requests.get(link)
        tree = html.fromstring(url.text)
        page = Page(link, True)
        current = TNode(page, parent, None)
        children = []
        for x in tree.xpath('//a/@href'):
            print(".")
            if(x.find("mailto")!=-1):
                newPage = Page(url, False)
                children.append(TNode(newPage, current, None))
				
            elif(x.find(".com")!=-1 or x.find(".org")!=-1 or x.find(".net")!=-1or x.find(".edu")!=-1 and x.find("club_find") ==-1):

                if(x.find("http:")==-1 and x.find("https:")==-1):
                    url = "http:"+x
                else:
                    url = x

                test = testUrl(url)
                newPage = Page(url, test)
                children.append(TNode(newPage, current, None))
        current.children = children
            #else:
                #print("not a url")
        return current
    else:
        return TNode(Page(link, False), parent, None)

#algorithm for make site function
#while link is on uccs domain
#if page.passed is true
#make page
#move onto children
def makeSite(link):
    root = makePage(link, None)
    makeSiteHelper(root)
    return root
def makeSiteHelper(current):
    if current.page.isOnDomain():
        if(current.children is not None):
            for x in current.children:
                if(x.page.isOnDomain()):
                    finished_links.append(x.page.url)#keeps track of links we have looked at

                    print("page: "+x.page.url)
                    print("######################")
                    x = makePage(x.page.url, current)
            for x in current.children:
                if(finished_links.count(x.page.url)< 3):
                   # temp = current.children.pop()
                    #current.children.append(temp)
                    makeSiteHelper(x)
                else:
                    print("url already finished")
    else:
        return
failed_links_messages = []
def validate(root):
    validateHelper(root)
def validateHelper(current):
    if(current.children is not None):
        for x in current.children:
            if x.page.passed:
               # temp = current.children.pop()
                #current.children.append(temp)
                validateHelper(x)

            else:
                message = x.parent.page.url + "this page failed to load URL; "+x.page.url
                failed_links_messages.append(message)
                print(message)

#array of sites you want scanned. probably a bit redundant
#links = {'http://sll.uccs.edu/', 'http://sll.uccs.edu/org/sga', "http://sll.uccs.edu/org/osa", "http://sll.uccs.edu/org/commute",
#         "http://sll.uccs.edu/org/liveleadership", "http://sll.uccs.edu/org/lobbies", "http://radio.uccs.edu/" , "http://sll.uccs.edu/org/uccslead"}
links  = {"http://sll.uccs.edu/","http://sll.uccs.edu/org/lobbies","http://sll.uccs.edu/org/liveleadership" }
print("Building site: ")
for x in links:
    root = makeSite(x)
    validate(root)
    print("Finished URL: "+x)
    print("----------------------------------")
    print("Validation:")
    for x in failed_links_messages:
        print(x)
print("Site tree complete")
print("Validation complete")
print("*********************************************************")
print("FULL LIST OF FAILED LINKS: ")
for x in failed_links_messages:
    print(x)
