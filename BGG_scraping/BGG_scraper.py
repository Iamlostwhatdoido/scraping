from bs4 import BeautifulSoup
import urllib3


with open("BGG_scraping/game_IDs.txt","r") as file:
    ID_list = file.read().splitlines()

with open("BGG_scraping/scrapped_data.txt", "w") as outfile:
	
	http = urllib3.PoolManager()

	for id in ID_list:
		
		url = "https://boardgamegeek.com/xmlapi/boardgame/"+str(id)+"?stats=1"
		response = http.request('GET',url)
		
		soup = BeautifulSoup(response.data,"xml")

		rank = soup.find("rank",type='subtype')['value']
		rating = soup.find("average").string

		complexity = soup.find("averageweight").string
		min_time = soup.find("minplaytime").string
		max_time = soup.find("maxplaytime").string

		players = str(soup.find("poll-summary").contents[3]['value'])
		players = players.replace('Recommended with ','').replace(' players','').replace('+','').split('–')
		
		if len(players)==1:
			min_player = players[0]
			max_player = players[0]
		else:
			min_player, max_player = players[0], players[1]

		best_player = str(soup.find("poll-summary").contents[1]['value'])
		best_player = best_player.replace('Best with ','').replace(' players','')

		outfile.write('\t'.join([	id,
						   			rank,
									rating,
									complexity,
									min_time,
									max_time,
									min_player,
									max_player,
									best_player]))
		
		if id != ID_list[-1]:
			outfile.write('\n')