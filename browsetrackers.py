#!/usr/bin/python2.6

# Script to search among private trackers
# See README.md

# Imports
from BeautifulSoup import BeautifulSoup
import urllib, re, os, sys
from optparse import OptionParser
import json
import ConfigParser

# Check arguments
parser = OptionParser()
parser.add_option("-v", "--verbose",
                  action="store_true", dest="isVerbose",
                  help="be verbose")

(options, args) = parser.parse_args() # list of options & positional arguments

if len(args) != 1:
    parser.error("incorrect number of arguments")
isVerbose = options.isVerbose
searchQuery = args[0]

# Scraping functions parse a HTML page and return selected elements as a set
def scrap_baconbits(htmlPage):
    torrents = [] # define empty list, same as var = list()
    soup = BeautifulSoup(htmlPage)
    for torrent in soup.findAll('tr', {'class' : re.compile("torrent ")}):
        torrentDetails = {} # define empty dictionary
        linkElement = torrent.find('a', {'title' : True, 'href' : re.compile("^torrents.php\?id\=")})
        torrentDetails['title'] = linkElement.string
        torrentDetails['torrentPage'] = linkElement['href']
        downloadLink = torrent.find('a', {'href' : re.compile("^torrents.php\?action\=download")})['href']
        torrentDetails['downloadLink'] = downloadLink
        torrentDetails['size'] = torrent.findAll('td')[4].string
        torrentDetails['seeds'] = torrent.findAll('td')[7].string
        torrents.append(torrentDetails)
    return torrents

def scrap_iplay(htmlPage):
    torrents = [] # define empty list, same as var = list()
    soup = BeautifulSoup(htmlPage)
    resTable = soup.find('table', { 'width' : '880px', 'border' : '0', 'cellspacing' : '0', 'cellpadding' : '0'})
    if resTable != None:
        for torrent in resTable.findAll('tr'):
            if torrent == resTable.find('tr'):
                continue # ignore first row, it's the header
            torrentDetails = {} # define empty dictionary
            torrentDetails['title'] = torrent.find('td', { 'class' : 'tabname' }).a['title']
            torrentDetails['torrentPage'] = torrent.find('td', { 'class' : 'tabname' }).a['href']
            torrentDetails['downloadLink'] = torrent.find('a', { 'title' : re.compile('^Download:') })['href']
            torrentDetails['size'] = "{0} {1}".format(torrent.findAll('td')[4].contents[0],  torrent.findAll('td')[4].contents[2])
            torrentDetails['seeds'] = torrent.findAll('td')[6].text
            torrents.append(torrentDetails)
    return torrents

def scrap_myanonamouse(htmlPage):
    torrents = [] # define empty list, same as var = list()
    soup = BeautifulSoup(htmlPage)
    resTable = soup.find('table', {'width' : '100%', 'cellspacing' : '1', 'class' : 'coltable'})
    if resTable != None:
        for row in resTable.findAll(lambda tag: tag.name == 'tr' and not tag.attrs): # torrents are only in <tr>s without attributes
            if row == resTable.find('tr'):
                continue # ignore first row, it's the header
            rowData = row.findAll('td', {'class' : 'row2'}) # torrent info is in class="row2" of <td>s
            if (len(rowData) == 10): # then it contains link to details and title
                torrentDetails = {} # define empty dictionary
                torrentDetails['title'] = rowData[1].a['title']
                torrentDetails['torrentPage'] = rowData[1].a['href']
                torrentDetails['downloadLink'] = 'NA'
                torrentDetails['size'] = rowData[6].text
                torrentDetails['seeds'] = rowData[8].text
                torrents.append(torrentDetails)
    return torrents

def scrap_demonoid(htmlPage):
    torrents = [] # define empty list, same as var = list()
    soup = BeautifulSoup(htmlPage)
    resTable = soup.find('table', {'width' : '100%', 'border' : '0', 'cellpadding' : '0', 'cellspacing' : '0', 'class' : 'font_12px'})
    for row in resTable.findAll(lambda tag: tag.name == 'tr' and not tag.attrs): # torrents are only in <tr>s without attributes
        rowData = row.findAll('td') # we want to process the table in paired rows, as each torrent info is split into two <td>s
        if (len(rowData) == 2): # then it contains link to details and title
            torrentDetails = {} # define empty dictionary
            torrentDetails['title'] = rowData[1].a.text
            torrentDetails['torrentPage'] = rowData[1].a['href']
        if (len(rowData) == 9): # then it contains size, seeds, etc
            torrentDetails['downloadLink'] = rowData[2].a['href']
            torrentDetails['size'] = rowData[3].text
            torrentDetails['seeds'] = rowData[6].text
            torrents.append(torrentDetails)
    return torrents

def scrap_theswarm(htmlPage):
    torrents = [] # define empty list, same as var = list()
    soup = BeautifulSoup(htmlPage)
    resTable = soup.find("table", "torrent_table")
    if resTable != None:
        for row in resTable.findAll('tr', { 'class' : re.compile("group_torrent.*") }):
            if row == resTable.find('tr'):
                continue # ignore first row, it's the header
            rowData = row.findAll('td')
            if (len(rowData) == 7): # then it contains our data
                torrentDetails = {} # define empty dictionary
                torrentDetails['title'] = rowData[0].findAll('a')[2]['title']
                if torrentDetails['title'] == "":
                    torrentDetails['title'] = rowData[0].findAll('a')[2].text
                torrentDetails['torrentPage'] = rowData[0].findAll('a')[2]['href']
                torrentDetails['downloadLink'] = rowData[0].span.a['href']
                torrentDetails['size'] = rowData[3].text
                torrentDetails['seeds'] = rowData[5].text
                torrents.append(torrentDetails)
    return torrents
    
def scrap_tehconnection(htmlPage):
    torrents = [] # define empty list, same as var = list()
    soup = BeautifulSoup(htmlPage)
    resTable = soup.find("table", "torrent_table")
    if resTable != None:
        for row in resTable.findAll('tr', { 'class' : re.compile("group_torrent.*") }):
            rowData = row.findAll('td')
            if (len(rowData) == 8): # then it contains our data
                torrentDetails = {} # define empty dictionary
                torrentDetails['title'] = rowData[1].findAll('a')[2]['title']
                if torrentDetails['title'] == "":
                    torrentDetails['title'] = rowData[1].findAll('a')[2].text
                torrentDetails['torrentPage'] = rowData[1].findAll('a')[2]['href']
                torrentDetails['downloadLink'] = rowData[1].span.a['href']
                torrentDetails['size'] = rowData[4].text
                torrentDetails['seeds'] = rowData[6].text
                torrents.append(torrentDetails)
    return torrents
    
def scrap_isohunt(htmlPage):
    torrents = [] # define empty list, same as var = list()
    parsed = json.loads(htmlPage)
    if parsed['items']['list'] != None:
        for res in parsed['items']['list']:
            torrentDetails = {} # define empty dictionary
            torrentDetails['title'] = res['title']
            torrentDetails['torrentPage'] = res['link']
            torrentDetails['downloadLink'] = res['enclosure_url']
            torrentDetails['size'] = res['size']
            torrentDetails['seeds'] = res['Seeds']
            torrents.append(torrentDetails)
    return torrents
    
def scrap_sceneaccess(htmlPage):
    torrents = [] # define empty list, same as var = list()
    soup = BeautifulSoup(htmlPage)
    resTable = soup.find("table", { 'id' : 'torrents-table' })
    if resTable != None:
        for row in resTable.findAll('tr', { 'class' : 'tt_row' }):
            rowData = row.findAll('td')
            if (len(rowData) == 9): # then it contains our data
                torrentDetails = {} # define empty dictionary
                torrentDetails['title'] = rowData[1].a['title']
                torrentDetails['torrentPage'] = rowData[1].a['href']
                torrentDetails['downloadLink'] = rowData[2].a['href']
                torrentDetails['size'] = rowData[3].contents[0]
                torrentDetails['seeds'] = rowData[7].text
                torrents.append(torrentDetails)
    return torrents

def scrap_test(htmlPage):
    titles = set()
    soup = BeautifulSoup(htmlPage)
    # <label for="cat_1">Music</label>
    for link in soup.findAll('label', {'for' : re.compile("^cat_[0-9]$")}):
        title = link.string
        titles.add(title)
    return titles

# /!\ Change the cookie properties in the config file  /!\    
# Read cookies config
Config = ConfigParser.ConfigParser()
Config.read("browsetrackers.ini")

# Define each tracker
trackers = [
            # BaconBits
            {'name' : 'BaconBits',
             'active' : 1,
             'cookie' : Config.get('Cookies', 'BaconBits'),
             'searchURL' : 'https://baconbits.org/torrents.php?order_by=s6&order_way=DESC&disablegrouping=1&action=advanced&torrentname={0}',
             'scraper' : scrap_baconbits
            },
            # TehConnection
            {'name' : 'TehConnection',
             'active' : 1,
             'cookie' : Config.get('Cookies', 'TehConnection'),
             'searchURL' : 'https://tehconnection.eu/torrents.php?order_by=s6&order_way=DESC&torrentname={0}',
             'scraper' : scrap_tehconnection
            },
            # SceneAccess
            {'name' : 'SceneAccess',
             'active' : 1,
             'cookie' : Config.get('Cookies', 'SceneAccess'),
             'searchURL' : 'https://www.sceneaccess.org/browse?search={0}&method=2',
             'scraper' : scrap_sceneaccess
            },
            # iPlay
            {'name' : 'iPlay',
             'active' : 1,
             'cookie' : Config.get('Cookies', 'iPlay'),
             'searchURL' : 'http://www.iplay.ro/browse.php?sort=seeders&d=DESC&search={0}',
             'scraper' : scrap_iplay
            },
            # The Swarm
            {'name' : 'TheSwarm',
             'active' : 0,
             'cookie' : None,
             'searchURL' : 'https://theswarm.me/torrents.php?order_way=asc&order_by=seeders&searchstr={0}',
             'scraper' : scrap_theswarm
            },
            # IsoHunt
            {'name' : 'IsoHunt',
             'active' : 1,
             'cookie' : None,
             'searchURL' : 'https://ca.isohunt.com/js/json.php?ihq={0}&rows=20&sort=seeds',
             'scraper' : scrap_isohunt
            },
            # Demonoid
            {'name' : 'Demonoid',
             'active' : 1,
             'cookie' : Config.get('Cookies', 'Demonoid'),
             'searchURL' : 'http://www.demonoid.ph/files/?to=1&sort=S&query={0}',
             'scraper' : scrap_demonoid
            },
            # My Anonamouse
            {'name' : 'MyAnonamouse',
             'active' : 1,
             'cookie' : Config.get('Cookies', 'MyAnonamouse'),
             'searchURL' : 'http://www.myanonamouse.net/browse.php?sort=7&type=desc&search={0}',
             'scraper' : scrap_myanonamouse
            },
            # Local gazelle
            {'name' : 'Gazelle',
             'active' : False,
             'cookie' : 'session=ZoB7LfxuKVWzSgpOkTvmAgxNsv3vZkLHHaEivGnHb%2FBOtxKhAz1zybjUx258e4E9qk667ZqR3RUVw2P3DgcnWQcKa%2FPcFJSKfAYjwg%2B2SD0SRZo3NpmnXtj4Yl0yYn%2BFcdw7UsQrVn35c4%2B1JoL82A%3D%3D;',
             'searchURL' : 'http://localhost:8888/e/gazelle/torrents.php?searchstr={0}',
             'scraper' : scrap_test
            },
            ]

# Browse one tracker for a torrent
def browseTracker(tracker, searchQuery):
    try:
        print ''
        print "Browsing {0}...".format(tracker['name'])
        # Create URL opener
        trackerURL = urllib.URLopener()
        # Set cookie
        if tracker['cookie'] != None:
            trackerURL.addheader('Cookie', tracker['cookie'])
            if isVerbose: print 'Cookie added [{0}]'.format(tracker['cookie'])
        # Open the search URL
        searchURL = tracker['searchURL'].format(searchQuery)
        if isVerbose: print 'searchURL [{0}]'.format(searchURL)
        htmlResults = trackerURL.open(searchURL)
        # Scrap HTML page with the tracker's scraper
        scraperFunction = tracker['scraper']
        torrents = scraperFunction(htmlResults.read())
        # Print list
        if not torrents:
            print "Nothing found in {0} :(".format(tracker['name'])
        else:
            for t in torrents:
                print '{0:100}[{1:10}][{2:4}]'.format(t['title'][:98].encode('utf8'), t['size'], t['seeds'])
        trackerURL.close()
    except Exception, msg:
                print "Exception with {0}: {1}".format(tracker['name'] ,str(msg))

#
# Main:
#

print ''
print 'Browsing trackers for "{0}"'.format(searchQuery)
# Replace spaces by '+'
searchQuery = re.sub('([ ])', '%20', searchQuery)

# For each defined tracker
for tracker in trackers:
    # Browse the tracker only if active
    if (tracker['active'] == True):
        browseTracker(tracker, searchQuery)
