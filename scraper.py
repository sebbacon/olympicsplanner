import urllib2
from lxml.etree import fromstring
from lxml.etree import tostring
from lxml.etree import HTMLParser
import csv

url = "http://olympic2012schedule.telegraph.co.uk/search/new?page=%d&sport=%d"

parser = HTMLParser()

outfile = csv.writer(open('schedule.csv', 'w'))
gendered = {}

for sportid in range(1, 42):
    page = 1
    while page:
        print url % (page, sportid)
        thing = fromstring(urllib2.urlopen(
            url % (page, sportid)).read(),
                           parser)
        items = thing.xpath('//table[contains(@class,"session-table")]')
        for item in items:
            date = item.xpath('.//td[@class="td-1"]/strong')[0].text
            medal_session = bool(item.xpath('.//span[contains(@class,"medal-session")]'))
            sport = item.xpath('.//p[@class="sport-title"]/strong')[0].text
            sessions = item.xpath('.//td[@class="td-2"]/div/ul/li')
            slist = []
            for sess in sessions:
                gender = sess.xpath('.')[0].attrib['class']
                event = sess.xpath('./em')[0].text
                slist.append((gender, event))
                asd = gendered.setdefault(gender, [])
                asd.append(event)
            start_time = item.xpath('.//td[@class="td-3"]')[0].text
            end_time = item.xpath('.//td[@class="td-4"]')[0].text
            location_bits = item.xpath('.//td[@class="td-5"]')[0]
            session_code = location_bits.xpath('.//span[@class="session-code"]')[0]
            limit = location_bits.xpath('.//span[@class="ticket-limit"]')[0].text
            location = tostring(location_bits)[18:tostring(location_bits).find("<br")].strip()
            tickets = [x.text for x in item.xpath('.//tr[@class="tickets"]/td//span')]
            outfile.writerow([date, sport, medal_session, str(slist),
                              limit, location, tickets, start_time, end_time])

        if thing.xpath(".//a[@class='next_page']"):
            page += 1
        else:
            page = None
        gkeys = gendered.keys()
        print [(x, len(gendered[x])) for x in gkeys]
    print "====="
