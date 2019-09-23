#! python3

# script to extract collections data from AIX API Website, for daily data feed to eCDw warehouse
# jq8274 logon, defaults pre-fitlered to BusinessnessUnitId 19000730 (Collections)
# exracts 1 day of data, 3 days back from current date, due to Survey late arrival lag
# outputs .csv flat file with all chat columns minus session dumps
# creates file to local PC, naming nomenclature 'datayyyymmdd.csv'

# History
# Created 02/02/2016

import datetime
import urllib.request
import base64

outfmt="%Y%m%d"
url='http://iax.research.att.com/cgi-bin/touchcommerceapi/lscalls?ps=%s&pe=%s&&fields=7FF8FFFFFFFFFFFFFFFFFFFF1FFFF'
userid='UserFakeName'
passwd='FakeNewsPassword'

today=datetime.date.today()
pe=today.strftime(outfmt)
ps=(today - datetime.timedelta(3)).strftime(outfmt)
urlt = url % (ps, pe)

p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, urlt, userid, passwd)
auth_handler = urllib.request.HTTPBasicAuthHandler(p)

opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)
try:
    open('data%s.csv' % ps, 'wb').write(opener.open(urlt).read())
except IOError as e:
    print(e)
