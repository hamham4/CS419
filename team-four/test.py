import httplib
import urllib
import json

sample1 = '{"request": {"type": "findTime","startYear": "2014","endYear": "2014","startMonth": "08","endMonth": "08","startDay": "21","endDay": "21","startTime": "09:30","endTime": "13:30","attendees": {"attendee": [{"username": "thorups"},{"username": "siplec"},{"username": "busherir"}]}}}'

params = urllib.urlencode({'request': sample1})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPConnection("team-four.appspot.com/submit")
conn.request("POST", "", params, headers)
response = conn.getresponse()