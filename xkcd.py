import urllib
from bs4 import BeautifulSoup as Soup
import lxml

class InvalidLinkException(Exception):

	def __init__(self, value):
		self.parameter = value

	def __str__(self):
		return repr(self.parameter)


class xkcd(object):

	def __init__(self):
		try:
			xkcdHtml = urllib.urlopen("http://xkcd.com/archive").read()
			self.soup = Soup(xkcdHtml, "lxml")
			link_set = self.soup.findAll('a')
			self.comic_set = [(comic.get('href')[1:-1], "http://xkcd.com" + comic.get('href'), comic.text, "http://www.explainxkcd.com/wiki/index.php/" + comic.get('href')[1:-1]) 
							  for comic in link_set 
							  if comic.get('href')[1:-1].isdigit()]
			self.current_comic_details()
		except Exception:
			print 'Please turn on your internet connection'

	def current_comic_details(self):
		self.current_comic_number = str(self.comic_set[0][0])
		self.current_comic_link = str(self.comic_set[0][1])
		self.current_comic_title = str(self.comic_set[0][2])
		self.current_comic_explain = str(self.comic_set[0][3])

	def get_comic(self, comic_num):
		try:
			if comic_num == 404:
				raise InvalidLinkException('xkcd is too cool to use comic #404')
			if comic_num > int(self.current_comic_number):
				raise InvalidLinkException('The current comic is #' + self.current_comic_number)
			try:
				comicHtml = urllib.urlopen("http://xkcd.com/" + str(comic_num)).read()
			except Exception:
				print 'Please turn on your internet connection'
			comic_soup = Soup(comicHtml)
			comic_img_list = comic_soup.findAll('img')
			comic_title = comic_img_list[1].get('alt')
			comic_img = comic_img_list[1].get('src')
			comic_desc = comic_img_list[1].get('title')
			comic_explain = "http://www.explainxkcd.com/wiki/index.php/" + str(comic_num)
			return (comic_img, comic_title, comic_desc, comic_explain)
		except InvalidLinkException, (instance):
			print instance.parameter
