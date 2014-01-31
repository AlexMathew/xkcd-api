import urllib
from bs4 import BeautifulSoup as Soup

class xkcd(object):

	def __init__(self):
		xkcdHtml = urllib.urlopen("http://xkcd.com/archive").read()
		self.soup = Soup(xkcdHtml)
		link_set = self.soup.findAll('a')
		self.comic_set = [(comic.get('href')[1:-1], "http://xkcd.com" + comic.get('href'), comic.text) 
						  for comic in link_set 
						  if comic.get('href')[1:-1].isdigit()]
		self.current_comic_details()

	def current_comic_details(self):
		self.current_comic_number = str(self.comic_set[0][0])
		self.current_comic_link = str(self.comic_set[0][1])
		self.current_comic_title = str(self.comic_set[0][2])