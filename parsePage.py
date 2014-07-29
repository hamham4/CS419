# Chris Siple
# CS 419 - Final Project: Group 4
# References: Beautifulsoup documentation/tutorial pages

from bs4 import BeautifulSoup
from urllib.request import urlopen

BASE_URL = "http://catalog.oregonstate.edu/"
ADD_URL = "&columns=jk"

def make_soup(url):
	html = urlopen(url).read()
	return BeautifulSoup(html, "lxml")

def get_dept_links(section_url):
	soup = make_soup(section_url)
	dlSubjects = soup.find(id = "ctl00_ContentPlaceHolder1_dlSubjects")
	dept_links = [BASE_URL + a["href"] for a in dlSubjects.findAll("a")]
	return dept_links

def get_data(links):
	for url in range(len(links)):
		soup2 = make_soup(links[url]+ADD_URL)
		table = soup2.find(id = "ctl00_ContentPlaceHolder1_dlCourses")
		for div in table.findAll('div'):
			data = div.findAll('td')
			name = data[0]
			sched = data[1]
			for br in sched.findAll('br'):
				br.replace_with(" ")
			#strips out Staff and TBA entries from catalog 
			if name.get_text() == "Staff" or sched.get_text().strip() == "TBA":
				continue
			print (name.get_text().strip(), sched.get_text().strip())
	return 1
		

links = get_dept_links("http://catalog.oregonstate.edu/SOC.aspx?level=all&campus=corvallis&term=201500")
success = get_data(links)



#for url in range(len(links)):
#	print(url,links[url])
	

