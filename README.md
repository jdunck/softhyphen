A web services for hyphenating text, powered by Google AppEngine.

Any HTTP POST will do, but here's a python example:

>>> import httplib2
>>> from urllib import urlencode
>>> h = httplib2.Http()
>>> r,c=h.request('http://www.softhypen.com/api', 'POST', urlencode({'lang':'en-us','content':'this is a lightweight test.'}))
>>> c
'this is a light&shy;weight test.'

## Dictionaries

This code utilizes the OpenOffice dictionaries found on this page: http://wiki.services.openoffice.org/wiki/Dictionaries

## Credits

This code stands on the shoulders of:

* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
* [Python Hyphenator](http://code.google.com/p/python-hyphenator/)
