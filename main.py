from pySiteUtils import makeSite,spellCheckTree, makeSitemap, printSitemap
import string

def run(link, domain):
    print("Building site: ")
    root = makeSite(link, domain)
    print("Site built")
    return root
def uccsDictFilter(s):
    rejects = ["uccs","edu","studlife","Bayer","Wienholtz","Cucchiara","Cohe","Frazier","Keener",
               "Bates","Bowen","Coppa","Edstrom","Ericson",'Hillmann','Merrifield','Mientka',
               'Pattirane','Schulman','Stickney','Tafoya','Wilson','doc','docx']
    if s[0] in string.ascii_uppercase and s[1] in string.ascii_uppercase:
        return False
    elif s in rejects:
        return False

    return True
#turns the pages from spellCheckTree into a single array
def processSpellCheck(pages, str=[]):
    if pages is not None:
        for i in pages:
            isfirst = True
            for chkr in i:
                if chkr is not None:
                    if(isfirst):
                        str.append(chkr)#the first index is not a checker. it is the url
                        print(chkr)
                        isfirst = False
                    else:
                        temp=[]
                        [temp.append(err.word) for err in chkr]
                        for word in filter(uccsDictFilter,temp):
                            str.append(word)
                            print(word)
    return str
#array of sites you want scanned. probably a bit redundant
link = "http://sll.uccs.edu"
domain = "sll.uccs.edu"
root = run(link, domain)
#pages = spellCheckTree(root)
#processSpellCheck(pages)
sitemap = makeSitemap(root)
printSitemap(sitemap)