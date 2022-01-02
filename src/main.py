#Libraries
import requests 
from bs4 import BeautifulSoup
from requests_html import HTMLSession

#Constants
DAILY_LINEUP_URL = "https://www.rotowire.com/basketball/nba-lineups.php"
STARTING_PLAYERS = []
POINTS = 1
REBOUNDS = 1.2
ASSISTS = 1.5
STEALS = 3
BLOCKS = 3
TURNOVERS = -1

#Create an HTML Session to render the web page JavaScript
createdSession = HTMLSession()
renderLineupPage = createdSession.get(DAILY_LINEUP_URL)
renderLineupPage.html.render()

#Parse through the page HTML using the BeautifulSoup library
mainPage = BeautifulSoup(renderLineupPage.html.html, "html.parser")
nbaLineups = mainPage.find_all("div", class_ = "lineup__main")

#Update the STARTING_PLAYERS array with the players guaranteed to start for each team today
for lineup in nbaLineups:
    try:
        visitorGuaranteedStart = lineup.find("ul", class_ = "lineup__list is-visit").find_all("li", class_ = "lineup__player is-pct-play-100")
        for player in visitorGuaranteedStart:
            STARTING_PLAYERS.append([player.find("a").text, player.find("div", class_ = "lineup__pos").text, "visitor"])

        homeGuaranteedStart = lineup.find("ul", class_ = "lineup__list is-home").find_all("li", class_ = "lineup__player is-pct-play-100")
        for player in homeGuaranteedStart:
            STARTING_PLAYERS.append([player.find("a").text, player.find("div", class_ = "lineup__pos").text, "home"])
        
    except:
        pass
        
print(STARTING_PLAYERS)
