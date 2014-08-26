import json
import urllib2
import httplib



sample1 = '{"request": {"type": "findTime","startYear": "2014","endYear": "2014","startMonth": "08","endMonth": "08","startDay": "21","endDay": "21","startTime": "09:30","endTime": "13:30","attendees": {"attendee": [{"username": "driskilq"}]}}}'


params = urllib.urlencode({'request': sample1})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost:10080")
conn.request("POST", "/submit", params, headers)
response = conn.getresponse()
print response.read()