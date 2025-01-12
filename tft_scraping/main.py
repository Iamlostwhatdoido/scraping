from bs4 import BeautifulSoup
import urllib3

with open("scraping\\tft_scraping\champion_output.txt", "w") as champ_outfile, open("scraping\\tft_scraping\\trait_output.txt","w") as trait_outfile:
	
	http = urllib3.PoolManager()

	url = "https://tftactics.gg/champions/"
	response = http.request('GET',url)

	soup = BeautifulSoup(response.data,'html5lib')

	traits_dict = {}

	characters_list = soup.find("div", class_='characters-list').find_all("a")

	for character in characters_list:
		character_url = '/champions/zyra/'
		character_url = character['href']

		response = http.request('GET',"https://tftactics.gg"+character_url)
		soup = BeautifulSoup(response.data,'html5lib')


		name = str(soup.find("div", class_='character-portrait').h1.string).replace("TFT ","")
		
		items_tag = soup.find("div", class_='items-list').find_all("a", class_='characters-item')
		items = [tag.find('img')['alt'] for tag in items_tag]
		items = ", ".join(items)

		cost = soup.find("ul", class_="stats-list").li.contents[2]

		character_traits = soup.find_all("h4",string='Origin') + soup.find_all("h4",string='Class')
		
		for i in range(len(character_traits)):
			trait_name = character_traits[i].previous_sibling.string

			if not trait_name in traits_dict:
				levels = character_traits[i].parent.parent.parent.find_all("div",class_="ability-bonus-count")
				for k in range(len(levels)):
					levels[k] = levels[k].string
				traits_dict[trait_name] = " | ".join(levels)

			character_traits[i] = trait_name
		
		character_traits = ", ".join(character_traits)


		champ_outfile.write('\t'.join([name,
						   			cost,
									character_traits,
									items]))
		
		if character != characters_list[-1]:champ_outfile.write('\n')
	
	trait_names = list(traits_dict.keys())

	for trait_name in trait_names:
		trait_outfile.write('\t'.join([trait_name, traits_dict[trait_name]]))
		if trait_name != trait_names[-1] : trait_outfile.write('\n')
		


