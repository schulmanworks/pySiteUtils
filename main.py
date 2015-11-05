from pySiteUtils import makeSite,spellCheckTree
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

#array of sites you want scanned. probably a bit redundant
link = "http://sll.uccs.edu"
domain = "sll.uccs.edu"
root = run(link, domain)
pages = spellCheckTree(root)
if pages is not None:
    for i in pages:
        isfirst = True
        for chkr in i:
            if chkr is not None:
                if(isfirst):
                    print(chkr)#the first index is not a checker. it is the url
                    isfirst = False
                else:
                    temp=[]
                    [temp.append(err.word) for err in chkr]
                    [print(word) for word in filter(uccsDictFilter,temp)]
        print("--------------------------")