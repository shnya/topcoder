#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import urllib2
import MySQLdb
import re

db = MySQLdb.connect(user='topcoder', passwd='naM58nduBXSRzWKb', db='topcoder', charset='utf8')
cur = db.cursor()


xml = urllib2.urlopen('http://www.topcoder.com/tc?module=BasicData&c=dd_round_list').read()
soup = BeautifulSoup(xml)
for row in soup('row'):
    c = row.contents
    if c[3].contents[0] != "Single Round Match":
        continue
    round_id = c[0].contents[0]
    round_name = c[2].contents[0]
    m = re.search("SRM ([0-9\.]+)", round_name)
    if not m:
        continue
    if float(m.group(1)) < 144:
        continue
    
    cur.execute("INSERT INTO tcpractice_round (id,name) VALUES (%s,%s) ON DUPLICATE KEY UPDATE id = %s", (round_id,round_name,round_id))
