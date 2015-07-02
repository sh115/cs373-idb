# import copperf
# import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup
import time

url = 'http://espn.go.com/nba/teams'
r = requests.get(url)

soup = BeautifulSoup(r.text)
tables = soup.find_all('ul', class_='medium-logos')

teams = []
prefix_1 = []
prefix_2 = []
teams_urls = []
roster_urls = []

nba_players_dict = {}

for table in tables:
	lis = table.find_all('li')
	for li in lis:
		current_team = li.h5.a.text
		infos = li.find_all('span')
		# haha = 0
		for info in infos:
			# print(haha)
			# haha += 1
			# print ("info")
			# if 'Roster' in info.text:
			# 	roster_urls.append(info.text)
			info1 = info.find_all('a')
			for span in info1:
				if 'Roster' in span.text:
					roster_url = 'http://espn.go.com' + span['href']
					# print(roster_url)
					# sys.exit()
					roster_urls.append(roster_url)
					time.sleep(1)
					roster_page = requests.get(roster_url)
					roster_page_soup = BeautifulSoup(roster_page.text)
					# print(roster_page_soup)
					# sys.exit()
					odd_players = roster_page_soup.find_all('tr', class_='oddrow')
					even_players = roster_page_soup.find_all('tr', class_='evenrow')
					all_players = []
					odd_players_iterate = iter(odd_players)
					even_players_iterate = iter(even_players)
					try: #121 #1212
						while True:
							all_players.append(next(odd_players_iterate))
							all_players.append(next(even_players_iterate))
					except StopIteration:
						pass
					print("players length: " + str(len(all_players)))

					for v in all_players:
						player_dic = {}

						print() #new line for new player
						print("Player team: " + current_team)
						player_dic['current_team'] = current_team
						player_stats = v.find_all('td')
						iterate = iter(player_stats)
						number = next(iterate)
						print("Player Number: " + str(number.text))
						player_dic['player_number'] = number.text
						player_name = next(iterate).a #gets the <a href> object
						print("Player Name: " + str(player_name.text))
						position = next(iterate)
						print("Player Position: " + str(position.text))
						player_dic['position'] = position.text
						age = next(iterate)
						print("Player age: " + str(age.text))
						height = next(iterate)
						player_dic['age'] = age.text
						print("Player Height: " + str(height.text))
						weight = next(iterate)
						player_dic['weight'] = weight.text
						print("Player weight: " + str(weight.text))
						college = next(iterate)
						if len(college.text) == 1:
							print("Player college: N/A")
							player_dic['college'] = 'N/A'
						else:
							print("Player college: " + str(college.text))
							player_dic['college'] = college.text
						salary = next(iterate)
						# if len(salary.text) == 1:
						# 	print("Player salary: N/A")
						# else:
						# 	print("Player salary: " + str(salary.text))

						#now we want to go to player page and get more information
						player_page = requests.get(player_name['href'])
						player_page_soup = BeautifulSoup(player_page.text)
						headshot_tag = player_page_soup.find_all('div', class_='main-headshot')
						player_headshot = None
						for v in headshot_tag:
							player_headshot = v.img
						
						if player_headshot == None: 
							#if player doesn't have headshot
							#assume not on the team, new draft
							#don't add to the json file
							#DO CONTINUE TO MOVE ONTO NEXT PLAYER AND DON'T ADD TO DICTIONARY!
							print("Player picture URL Not Available")
							continue #skip the youtube part because is this year's draft. not in the nba most recent season.
						else:
							print("Player picture URL: " + player_headshot['src'])
							player_dic['picture'] = player_headshot['src']
							#you know in nba last season
							#so just print out all the usual stats
							#get birth date
							#get experience
							#get ppg, apg, rpg, per, 
							#and career ppg, apg, rpg
							player_life_info = player_page_soup.find_all('ul', class_='player-metadata floatleft')
							player_life_info_list = player_life_info[0].find_all('li')
							#set it all up
							player_dic['birth_info'] = 'N/A'
							player_dic['draft info'] = 'N/A'
							player_dic['experience_info'] = 'N/A'
							for v in player_life_info_list:
								if "Born" in v.text:
									birth_info = v.text[4:]
									print("Birth info: " + birth_info)
									player_dic['birth_info'] = birth_info
								if "Drafted" in v.text:
									drafted_info = v.text[7:]
									print("Drafted Info: " + drafted_info)
									player_dic['draft_info'] = drafted_info
								if "Experience" in v.text:
									experience_info = v.text[10:]
									print("Experience info: " + experience_info)
									player_dic['experience_years'] = experience_info

							player_header_stats_element = player_page_soup.find_all('table', class_='header-stats')
							if len(player_header_stats_element) == 0:
								continue
							else: 
								player_header_stats_element = player_header_stats_element[0]
							# print(len(player_header_stats_element))
							# sys.exit()
							player_header_stats_check = player_header_stats_element.find_all('tr')[0]
							player_header_stats_stats = player_header_stats_check.find_all('td')
							iterate = iter(player_header_stats_stats)
							ppg = next(iterate).text
							print("Points per game: " + ppg)
							player_dic['ppg'] = ppg
							rpg = next(iterate).text
							print("Rebounds per game: " + rpg)
							player_dic['rpg'] = rpg
							blkpg = next(iterate).text
							print("Blocks per game: " + blkpg)
							player_dic['blkpg'] = blkpg
							per = next(iterate).text
							print("Player Efficiency Rating: " + per)
							player_dic['per'] = per

							#now get career ppg, apg, and rpg
							player_career_element = player_page_soup.find_all('tr', class_='career')[0]
							player_career_stats = player_career_element.find_all('td')
							iterate = iter(player_career_stats)
							career_ppg = next(iterate).text
							print("Career Points per game: " + career_ppg)
							player_dic['career_ppg'] = career_ppg
							career_rpg = next(iterate).text
							print("Career Rebounds per game: " + career_rpg)
							player_dic['career_rpg'] = career_rpg
							career_blkpg = next(iterate).text
							print("Career Blocks per game: " + career_blkpg)
							player_dic['career_blkpg'] = career_blkpg

						#USE CONTINUE
						#We're on player page
						print

						#Get some youtube links!
						#put into a list
						player_youtube = requests.get('https://www.youtube.com/results?search_query=' + player_name.text + 'highlights')
						player_youtube_soup = BeautifulSoup(player_youtube.text)
						# print(player_youtube_soup)
						# sys.exit()
						player_youtube_links = player_youtube_soup.find_all('a', class_='yt-uix-sessionlink        spf-link ')
						num_vids = 3
						num_count = 0
						youtube_links_list = []
						for v in player_youtube_links:
							if num_count == num_vids:
								break
							print("Player Youtube Video " + str(num_count) + ": " + 'https://www.youtube.com' + v['href'])
							youtube_links_list += ['https://www.youtube.com' + v['href']]
							num_count += 1

						player_dic['youtube_links'] = youtube_links_list
						#add to dictionary at the very end!
						nba_players_dict[player_name.text] = player_dic

						#GET TWITTER FEEDS
						#SEARCHES ON TWITTER NAME, AND ASSUMES
						#IF IT FINDS VERIFIED, THEN THAT IS IT
						player_first_name = player_name.text[:player_name.text.index(' ')]
						player_last_name = player_name.text[player_name.text.index(' ') + 1:]
						twitter_search_page = requests.get('https://twitter.com/search?q=' + player_first_name + '%20' + player_last_name + '&src=typd')
						twitter_search_soup = BeautifulSoup(twitter_search_page.text)
						verified_twitters = twitter_search_soup.find_all('span', class_='Icon Icon--verified')
						# print(twitter_search_soup)
						# sys.exit()
						player_dic['twitter'] = 'N/A'
						#if there is verified on here
						print_twitter_boolean = True
						for v_twitters in verified_twitters:
							twitter_link = twitter_search_soup.find_all('a', class_='ProfileCard-avatarLink js-nav js-tooltip')[0]
							twitter_player_url = 'https://twitter.com' + twitter_link['href']
							print("Twitter_Player_url: " + twitter_player_url)
							player_dic['twitter'] = twitter_player_url
							print_twitter_boolean = False
							break

						if print_twitter_boolean:
							print("Twitter_Player_url: N/A")


		#NEED PICTURES AND YOUTUBE LINKS, 3 YOUTUBE LINKS
		#AND PLAYER STATISTICS

		# teams.append(info.text)
		# url = info['href']
		# teams_urls.append(url)
		# prefix_1.append(url.split('/')[-2])
		# prefix_2.append(url.split('/')[-1])

dic = {'url': teams_urls, 'prefix_2': prefix_2, 'prefix_1': prefix_1}
# teams = pd.DataFrame(dic, index=teams)
# teams.index.name = 'team'

# print(teams)
# print (roster_urls)

print(nba_players_dict)

import json
with open('nba_players_data.json', 'w+') as outfile:
    json.dump(nba_players_dict, outfile)