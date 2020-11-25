import requests
import json
from bs4 import BeautifulSoup

# Main Dicts
full_season = {}
full_season_perf = {}

# Loop to access all url's
urls_lpl = [
            "https://lol.gamepedia.com/Riot_Season_2_Brazilian_Championship",
            "https://lol.gamepedia.com/Riot_Season_3_Brazilian_Championship",
            "https://lol.gamepedia.com/CBLOL/2014_Season/Regional_Finals",
            "https://lol.gamepedia.com/CBLOL/2014_Season/Champions_Series",
            "https://lol.gamepedia.com/CBLOL/2015_Season",
            "https://lol.gamepedia.com/CBLOL/2016_Season",
            "https://lol.gamepedia.com/CBLOL/2017_Season",
            "https://lol.gamepedia.com/CBLOL/2018_Season",
            "https://lol.gamepedia.com/CBLOL/2019_Season",
            "https://lol.gamepedia.com/CBLOL/2020_Season"
            ]

# Main loop
for url in urls_lpl:
    # Access to the main page for each url
    url_tournment = url
    response_tournment = requests.get(url_tournment)
    soup_tournment = BeautifulSoup(response_tournment.text, "html.parser")

    # Access to each season
    try:
        seasons = soup_tournment.find(class_="tabheader-top").findAll('a')
        eol_season = [season.get('href') for season in seasons if ("Picks_and_Bans" not in season.get('href')) and ("Qualifiers" not in season.get('href'))] 
    except:
        eol_season = [url]

    for eol in eol_season:
        names = {}
        names_perf = {}
        if url in eol_season:
            url_season = url
        else:
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