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
        if(self.url.find("sll.uccs.edu") == -1 ):#and self.url.find("radio.uccs.edu") == -1):#need to add all sll domains/sub-domains
            return False
        else:
            return True

def testUrl(link):
    try:
        words = ["404"]
        opener = urllib.request.urlopen(link)
        site = opener.read()
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
        current = TNode(page, parent, children=[])

        for x in tree.xpath('//a/@href'):
            print(".")
            if(x.find("mailto")!=-1):
                continue
                #newPage = Page(x, False)
                #current.children.append(TNode(newPage, current, None))
				
            elif(x.find(".com")!=-1 or x.find(".org")!=-1 or x.find(".net")!=-1or x.find(".edu")!=-1 and x.find("club_find") ==-1):

                if(x.find("http:")==-1 and x.find("https:")==-1):
                    x = "http:"+x

                test = testUrl(x)
                newPage = Page(x, test)
                current.children.append(TNode(newPage, current, None))

       
        return current
    else:
        return TNode(Page(link, False), parent, None)

#algorithm for make site function
#while link is on uccs domain
#if page.passed is true
#make page
#move onto children
def makeSite(link):
    print("######################")
    print("page: "+link)
    root = makePage(link, None)
    makeSiteHelper(root)
    return root
def makeSiteHelper(current):
    if current.page.isOnDomain():
        if(current.children is not None):
            i = 0
            for x in current.children:
                if(x.page.isOnDomain() and x.page.url not in finished_links and x.page.passed):
                    finished_links.append(x.page.url)#keeps track of links we have looked at
                    print("######################")
                    print("page: "+x.page.url)
                    tempPage = makePage(x.page.url, current)
                    current.children.insert(i,tempPage)
                    current.children.remove(x)
                    makeSiteHelper(tempPage)
                    i = 1+i

def printTree(root):
    printTreeHelper(root)
def printTreeHelper(current):
    if current is not None:
        print(current.page.url)
        if current.children is not None:
            for x in current.children:
                printTreeHelper(x)
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

                message = x.parent.page.url + "this page failed to load URL: "+x.page.url
                print(message)

#array of sites you want scanned. probably a bit redundant
#links = {'http://sll.uccs.edu/', 'http://sll.uccs.edu/org/sga', "http://sll.uccs.edu/org/osa", "http://sll.uccs.edu/org/commute",
#         "http://sll.uccs.edu/org/liveleadership", "http://sll.uccs.edu/org/lobbies", "http://radio.uccs.edu/" , "http://sll.uccs.edu/org/uccslead"}
#links  = {"http://sll.uccs.edu/","http://sll.uccs.edu/org/lobbies","http://sll.uccs.edu/org/liveleadership","http://sll.uccs.edu/org/clubhelp/" }
links={"http://sll.uccs.edu/"}
print("Building site: ")
for x in links:

    root = makeSite(x)

    print("Finished URL: "+x)
    print("----------------------------------")
    print("Validation:")
    validate(root)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("Printed Tree:")
    #printTree(root)
print("Process completed")
print("*********************************************************")