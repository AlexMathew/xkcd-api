import urllib
from bs4 import BeautifulSoup as Soup


class InvalidLinkException(Exception):

	def __init__(self, value):
		self.parameter = value

	def __str__(self):
		return repr(self.parameter)


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

	def get_comic(self, comic_num):
		try:
			if comic_num == 404:
				raise InvalidLinkException('xkcd is too cool to use comic #404')
			if comic_num > int(self.current_comic_number):
				raise InvalidLinkException('The current comic is #' + self.current_comic_number)
			comicHtml = urllib.urlopen("http://xkcd.com/" + str(comic_num)).read()
			comic_soup = Soup(comicHtml)
			comic_img_list = comic_soup.findAll('img')
			comic_img = comic_img_list[1].get('src')
			comic_title = comic_img_list[1].get('title')
			return (comic_img, comic_title)
		except InvalidLinkException, (instance):
			print instance.parameter