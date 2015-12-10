from pySiteUtils import printTree, validateURLs, makeSite, processSpellCheck, spellCheckTree, makeSitemap,printSitemap
import string

def run(link, domain):
    print("Building site: ")
    root = makeSite(link, domain)
    print("Site built")
    return root
def uccsDictFilter(s,x):
    print("s")
    print(s)
    print("x")
    print(x)
    rejects = ["uccs","edu","studlife","Bayer","Wienholtz","Cucchiara","Cohe","Frazier","Keener",
               "Bates","Bowen","Coppa","Edstrom","Ericson",'Hillmann','Merrifield','Mientka',
               'Pattirane','Schulman','Stickney','Tafoya','Wilson','doc','docx']
    if s[0] in string.ascii_uppercase and s[1] in string.ascii_uppercase:
        return False
    elif s in rejects:
        return False

    return True
    return str
#array of sites you want scanned. probably a bit redundant
link = "http://sll.uccs.edu/org/mlchelp"
domain = "sll.uccs.edu/org/mlchelp"
root = run(link, domain)
#map = makeSitemap(root)
#printSitemap(map)
#pages = spellCheckTree(root)
#processSpellCheck(pages, uccsDictFilter)
printTree(root)
print(validateURLs(root))