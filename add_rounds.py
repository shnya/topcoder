#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import urllib2
import MySQLdb

db = MySQLdb.connect(user='topcoder', passwd='naM58nduBXSRzWKb', db='topcoder', charset='utf8')
cur = db.cursor()


xml = urllib2.urlopen('http://www.topcoder.com/tc?module=BasicData&c=dd_algo_practice_rooms&dsid=30').read()
soup = BeautifulSoup(xml)
for row in soup('row'):
    c = row.contents
    round_id = c[0].contents[0]
    round_name = c[1].contents[0]
    cur.execute("INSERT INTO tcpractice_round (id,name) VALUES (%s,%s) ON DUPLICATE KEY UPDATE id = %s", (round_id,round_name,round_id))
