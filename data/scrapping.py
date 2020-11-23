import requests
import urllib.request
import time
from bs4 import BeautifulSoup

names = {}

url_tournment = 'https://lol.gamepedia.com/Champions/2015_Season/Summer_Playoffs'
response_tournment = requests.get(url_tournment)
soup_tournment = BeautifulSoup(response_tournment.text, "html.parser")

teams = soup_tournment.find(class_="tournament-rosters").findAll(class_='wikitable tournament-roster')

for team in teams:
    name_players = []
    end_link_team = team.find(class_="tournament-roster-header").find('a').get('href')

    url_team = "https://lol.gamepedia.com" + end_link_team
    response_team = requests.get(url_team)
    soup_team = BeautifulSoup(response_team.text, "html.parser")
    change = soup_team.find(class_="infobox-notice")
    
    while change != None:
        if change.string != "Team has disbanded.":
            new_link = change.find('a').get('href')
            url_team = "https://lol.gamepedia.com" + new_link
            response_team = requests.get(url_team)
            soup_team = BeautifulSoup(response_team.text, "html.parser")
            change = soup_team.find(class_="infobox-notice")
        else:
            break

    real_team_name = soup_team.find(class_="infobox-title").string

    players = team.findAll(class_="tournament-roster-player-cell")
    for player in players:
        end_link_player = player.find('a').get('href')

        url_player = "https://lol.gamepedia.com" + end_link_player
        response_player = requests.get(url_player)
        soup_player = BeautifulSoup(response_player.text, "html.parser")
        try:
            name_players.append(soup_player.find(class_="infobox-title").string)
        except:
            name_players.append(end_link_player)

    print(real_team_name)   

    names[real_team_name] = name_players

print(names)