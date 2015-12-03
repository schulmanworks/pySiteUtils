__author__ = 'ryan'
#!/usr/bin/env python

from distutils.core import setup
setup(name='Distutils',
      version='1.0',
      description='UCCS Dead Link Tester',
      author='Ryan Schulman',
      author_email='schulmanworks@gmail.com',
      url='http://sll.uccs.edu',
      packages=['distutils', 'distutils.command', 'urllib.request', 'lxml', 'html', 'requests'],
     )