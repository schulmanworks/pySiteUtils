__author__ = 'rschulma'
import urllib.request
import sys
from lxml import html
import requests
global finished_links
finished_links = []
class TNode(object): #Nodes of the tree. 1 parent, unlimited children via list
    def __init__(self, page, parent, children = []):
        self.page = page
        self.parent = parent
        self.children = children
    def hasChild(self):
        if len(self.children) != 0:
            return True
        else: return False

class Page(object):#when passed is true, the page has a 200 code. Otherwise it fails
    text = "Not yet set"
    def __init__(self,url, passed):
        self.url = url
        self.passed = passed

    def setText(self,text):
        self.text = text

    def isOnDomain(self):
        if(self.url.find("sll.uccs.edu") == -1 and self.url.find("uccs.edu/sll")==-1 and self.url.find("uccs.edu/sga")==-1):#and self.url.find("radio.uccs.edu") == -1):#need to add all sll domains/sub-domains
            return False
        else:
            return True

#tkaes a string
def testUrl(link):#test url for non 200 message
    try:
        opener = urllib.request.urlopen(link)
        site = opener.read()
        code = opener.getcode()

        if(code//100 == 2):#any code that starts with a 2
            return True
        else:
            return False
    except:
        return False
#takes a string and a node
def makePage(temp, parent):
    link = temp
    try:
        opener = urllib.request.urlopen(link)
        code = opener.getcode()
    except:
        return TNode(Page(link, False),parent,{None})

    if(code == 200):
       #
        url = requests.get(link)
        tree = html.fromstring(url.text)
        page = Page(link, True)
        current = TNode(page, parent, children=[])
        pageHasURLs = False
        #urlText = tree.xpath('//a/text()')
        urls = tree.xpath('//a/@href')
        urlText = tree.xpath('//a')
        for x,y in zip(urls,urlText):#for all the links in a page
            if(len(y.xpath('text()')) > 0):
                text = y.xpath('text()')[0]
                #print("url: "+x+"text: "+y.xpath('text()')[0])
            else:
                text = "none, may be an image"
                #print("url: "+x+"text: none, may be an image")
            pageHasURLs = True


            if(x.find("mailto")!=-1):#mailto links are ignored, remove continue and comment marks to mark them as failed instead
                continue
                #newPage = Page(x, False)
                #current.children.append(TNode(newPage, current, None))
				
            elif(x.find(".com")!=-1 or x.find(".org")!=-1 or x.find(".net")!=-1or x.find(".edu")!=-1 or x.find(".gov")!=-1
            or x.find(".info")!=-1 and x.find("club_find") ==-1):#if it's a link, and it's not under "find a club"

                if(x.find("http:")==-1 and x.find("https:")==-1):#make sure url has http
                    x = "http:"+x

                test = testUrl(x)
                newPage = Page(x, test)
                newPage.setText(text)
                current.children.append(TNode(newPage, current, None))

        if(not pageHasURLs):#tests for 404 pages that don't return a 404 error message. Will break if urls are added to 404 pages.
            current.page.passed = False

        return current
    else:
        return TNode(Page(link, False), parent, None)

#algorithm for make site function
#while link is on uccs domain
#if page.passed is true
#make page
#move onto children

#takes a URL
def makeSite(link):#make the website into a tree of urls
    print("######################")
    print("page: "+link)
    root = makePage(link, None)
    makeSiteHelper(root)
    return root
def makeSiteHelper(current):#takes a node
    if current.page.isOnDomain():
        if(current.children is not None):
            i = 0
            for x in current.children:
                if(x.page.isOnDomain() and x.page.url not in finished_links and x.page.passed):
                    finished_links.append(x.page.url)#keeps track of links we have looked at
                    print("page: "+x.page.url)
                    tempPage = makePage(x.page.url, current)#make page from child page
                    tempPage.page.setText(x.page.text)
                    current.children.insert(i,tempPage)#insert new page into location that once had child page
                    current.children.remove(x)#remove old child page
                    makeSiteHelper(tempPage)#move onto that child's children
                    i = 1+i#incrment list index

def printTree(root):#takes a node
    printTreeHelper(root)
def printTreeHelper(current):#takes a node
    if current is not None:
        print("%50s%-s",current.page.url,current.page.passed)
        if current.children is not None:
            for x in current.children:
                printTreeHelper(x)
global failed_links_messages
failed_links_messages = []
def validate(root):#takes a node
    validateHelper(root)
def validateHelper(current):#takes a node
    if(current.children is not None):
        for x in current.children:
            if x.page.passed:

                validateHelper(x)

            else:
                message = x.parent.page.url + " this page failed to load URL: "+x.page.url +" Link: "+x.page.text
                failed_links_messages.append(message)
                print(message)

#array of sites you want scanned. probably a bit redundant
links = {"http://sll.uccs.edu/","http://sll.uccs.edu/org/lobbies","http://sll.uccs.edu/org/liveleadership","http://sll.uccs.edu/org/sga","http://sll.uccs.edu/org/commute","http://sll.uccs.edu/org/uccslead"}#quick search

print("Building site: ")

for x in links:
    root = makeSite(x)
    print("Finished URL: "+x)
    print("----------------------------------")
    print("Validation:")
    validate(root)
    print("----------------------------------")
    #printTree(root)
    for y in links:#remove top level domains from finished links so they are listed as processed
        if(y in finished_links):
            finished_links.remove(y)
print("Process completed")
print("*********************************************************")

for str in failed_links_messages:
    print(str)