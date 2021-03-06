import requests
import json
from bs4 import BeautifulSoup

# Main Dicts
full_season = {}
full_season_perf = {}

# Loop to access all url's
urls_lck = [
            "https://lol.gamepedia.com/Champions/2012_Season",
            "https://lol.gamepedia.com/Champions/2013_Season",
            "https://lol.gamepedia.com/Champions/2014_Season",
            ]

# Main loop
for url in urls_lck:
    # Access to the main page for each url
    url_tournment = url
    response_tournment = requests.get(url_tournment)
    soup_tournment = BeautifulSoup(response_tournment.text, "html.parser")

    # Access to each season
    seasons = soup_tournment.find(class_="tabheader-top").findAll('a')
    eol_season = [season.get('href') for season in seasons if ("Qualifiers" not in season.get('href')) and ("Points" not in season.get('href'))]

    for eol in eol_season:
        names = {}
        names_perf = {}
        url_season = "https://lol.gamepedia.com" + eol
        response_season = requests.get(url_season)
        soup_season = BeautifulSoup(response_season.text, "html.parser")

        # Name and list of all teams
        tournment = soup_season.find(class_="firstHeading").string
        print("Acessando o {}".format(tournment))
        teams_brute = soup_season.find(class_="tournament-rosters").findAll(class_='wikitable tournament-roster')

        # Name of players and team (Team: [Players])
        for team in teams_brute:
            name_players = []
            eol_team = team.find(class_="tournament-roster-header").find('a')

            url_team = "https://lol.gamepedia.com" + eol_team.get('href')
            response_team = requests.get(url_team)
            soup_team = BeautifulSoup(response_team.text, "html.parser")
            change = soup_team.find(class_="infobox-notice")

            # If the team had a name change
            while change != None:
                if change.string != "Team has disbanded.":
                    new_link = change.find('a').get('href')
                    url_team = "https://lol.gamepedia.com" + new_link
                    response_team = requests.get(url_team)
                    soup_team = BeautifulSoup(response_team.text, "html.parser")
                    change = soup_team.find(class_="infobox-notice")
                else:
                    break

            try:
                real_team_name = soup_team.find(class_="infobox-title").string
            except:
                real_team_name = eol_team.string

            # Put all players of a team in a list and get last name
            players = team.findAll(class_="tournament-roster-player-cell")
            for player in players:
                end_link_player = player.find('a').get('href')

                url_player = "https://lol.gamepedia.com" + end_link_player
                response_player = requests.get(url_player)
                soup_player = BeautifulSoup(response_player.text, "html.parser")
                try:
                    name_players.append(soup_player.find(class_="infobox-title").string)
                except:
                    name_players.append(player.find('a').string)

            # Create (Team: [Players])
            names[real_team_name] = name_players
        # Create (Season: {Team[Players]})
        full_season[tournment] = names

with open('data/json/output.json', 'w', encoding='utf8') as json_file:
    json.dump(full_season, json_file, ensure_ascii=False)