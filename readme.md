This is a set of utilites that can help analyze a website. They are first added to pySiteUtils.py
for use in a command line interface or other project. They are then integrated into Flask.
This libary analyzes your website using an n-ary tree.

***********************************************************************************************
Installation:

Without Flask:
All you really need is the file pySiteUtils.py along with the libraries listed in the import section.
You can use main.py as an example of how to use the utilities.

With Flask:
Warning: All the features of this utility are not always integrated into Flask.
Install the necessary libaries listed at the top of pySiteUtils.py. Also install Flask and WTForms.
Run run.py and open the webpage as you would a normal Flask site.

***********************************************************************************************

Useful methods:
makeSite():
Creates an n-ary, parent referencing tree of all the pages ofyour website. This includes with URL
the domain it should be on, and whether or not it passed the check for that domain.
Returns the highest node of the tree.

printTree():
Prints everything below a given node made in makeSite().
Returns nothing.

validateURLS():
Validates all the urls below an input node.
Returns

spellCheckTree():
Spellchecks all the valid pages in the tree.
Returns

processSpellCheck():
Turns the pages from spellCheckTree into a single array
Returns that array

makeSitemap():


printSitemap():

