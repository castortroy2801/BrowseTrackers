What is this?
=
Python script to search among private trackers.

When using private trackers it's always painful to search for stuff one by one. This script scraps the results of running a search on previously configured trackers.

How to use
=
Usage : python browsetrackers.py "searched_terms" [-v|--verbose]

Example : python browsetrackers.py "ubuntu" [-v|--verbose]

To add/remove sites:

- Adapt/create scraper function as necessary.
- Add/change the cookie property of each tracker in the .ini file. In your browser,
look at the tracker's cookie, and copy/paste the relevant info.

Developer notes
=
I was going to use Tidy <http://tidy.sourceforge.net/> but iplay.ro has a really untidy HTML which results in error.

I was going to use HTMLParser <http://docs.python.org/release/2.6.7/library/htmlparser.html> but I understand it might need Tidy.

So I tried BeautifulSoup <http://www.crummy.com/software/BeautifulSoup> version 3.2.0, installed in /usr/lib/python2.6/site-packages/

First version snatched from <http://pastebin.com/f79240554>
Original author released it in <http://www.torrent-invites.com/bittorrent-discussion/47809-browsing-multiple-trackers.html>

There were cooler versions there (GUI, and Win32 execs) but his uploads to rapidshare got removed.

Documentation
=
- [BeautifulSoup official Doc](http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html)
- [Beginning in Python - From Novice to Professional](http://amzn.com/1590599829)

History
=
- 1.4 100512 - Moved cookie config to .ini file
- 1.3 090312 - Added JSON parsing for isohunt.com's API (<https://ca.isohunt.com/forum/viewtopic.php?t=150656>)
        Tried to make all connections https://
- 1.2 080312 - Added -v|--verbose mode with OptionParser
    - Fixed empty result sets bug when using soup.find() as initial fetcher (iplay, myanonamouse, ...)
    - All scrapers get same info now: title, torrentPage, downloadLink, size & seeds
- 1.1 080212 - Added scraping and display of torrent details: size, DL link, seeds...
- 1.1 080212 - Replace now puts ASCII 'space' instead of '+'
- 1.1 070212 - Removed download .torrent feature
    - Removed initial '+' in search term
    - Replaced RE formulas with scraping
- 1.0 070212 - Snatched from Youri36's version

TODO
=
- replace urllib with urllib2 (<http://docs.python.org/release/2.6.7/library/urllib2.html>)
- experiment with <http://ai-depot.com/articles/the-easy-way-to-extract-useful-text-from-arbitrary-html/>
- Rewrite OOed version with Python3 and BeautifulSoup4