from bs4 import BeautifulSoup
import urllib3

with open("scraping\letterbox_scraping\output.txt", "w") as outfile:
	
	http = urllib3.PoolManager()

	url = "https://letterboxd.com/film/beetlejuice-beetlejuice/"
	response = http.request('GET',url)
	
	soup = BeautifulSoup(response.data,"html5lib")

	print(soup.prettify())