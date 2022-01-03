#Libraries
import json
import requests 
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession

#Constants
DAILY_LINEUP_URL = "https://www.rotowire.com/basketball/nba-lineups.php"
MAIN_URL = "https://www.rotowire.com"
AJAX_INFO_URL = "https://www.rotowire.com/basketball/ajax/player-page-data.php?"
STARTING_PLAYERS = []
ALL_PG = []
ALL_SG = []
ALL_SF = []
ALL_PF = []
ALL_C = []
POINTS = 1
REBOUNDS = 1.2
ASSISTS = 1.5
STEALS = 3
BLOCKS = 3
TURNOVERS = -1


#Get the players guaranteed to start for each team today
def getStartingPlayers(playerList):

    #Create an HTML Session to render the web page JavaScript
    createdSession = HTMLSession()
    renderLineupPage = createdSession.get(DAILY_LINEUP_URL)
    renderLineupPage.html.render()

    #Parse through the page HTML using the BeautifulSoup library
    mainPage = BeautifulSoup(renderLineupPage.html.html, "html.parser")

    nbaLineups = mainPage.find_all("div", class_ = "lineup is-nba")

    #Get all relevant data for players that are guaranteed to start today and put them in an array
    for lineup in nbaLineups:
        try:
            visitorTeam = lineup.find("div", class_ = "lineup__teams").find("a", class_ = "lineup__team is-visit")['href'][-3:]
            visitorGuaranteedStart = lineup.find("ul", class_ = "lineup__list is-visit").find_all("li", class_ = "lineup__player is-pct-play-100")
            for player in visitorGuaranteedStart:
                playerList.append([player.find("a").text, player.find("div", class_ = "lineup__pos").text, "visitor", visitorTeam, player.find("a")['href']])

            homeTeam = lineup.find("div", class_ = "lineup__teams").find("a", class_ = "lineup__team is-home")['href'][-3:]
            homeGuaranteedStart = lineup.find("ul", class_ = "lineup__list is-home").find_all("li", class_ = "lineup__player is-pct-play-100")
            for player in homeGuaranteedStart:
                playerList.append([player.find("a").text, player.find("div", class_ = "lineup__pos").text, "home", homeTeam, player.find("a")['href']])
        except:
            pass


#Calculate weighted fantasy score for a player
def getFantasyScore(thirtySixAverage, starterMinutesExpected):
    try:
        points = ((thirtySixAverage[0] / 36.0) * starterMinutesExpected) * POINTS
        rebounds = ((thirtySixAverage[1] / 36.0) * starterMinutesExpected) * REBOUNDS
        assists = ((thirtySixAverage[2] / 36.0) * starterMinutesExpected) * ASSISTS
        steals = ((thirtySixAverage[3] / 36.0) * starterMinutesExpected) * STEALS
        blocks = ((thirtySixAverage[4] / 36.0) * starterMinutesExpected) * BLOCKS
        turnovers = ((thirtySixAverage[5] / 36.0) * starterMinutesExpected) * TURNOVERS
        return round(points + rebounds + assists + steals + blocks + turnovers, 2)
    except:
        print("Error: Player data is either missing or incorrectly formatted")


#Update the player array given by adding their expected fantasy score to the end
def addScore(player):
    playerInfo = []
    generalizedPosition = ""

    #Declare position of player in format that is acceptable to index in the JSON
    if(player[1] == "PG" or player[1] == "SG"):
        generalizedPosition = "G"
    elif(player[1] == "SF" or player[1] == "PF"):
        generalizedPosition = "F"
    else:
        generalizedPosition = "C"

    try:
        #Get AJAX stat page for the given player and convert it from JSON to a Python Dictionary object
        playerURL = AJAX_INFO_URL + "id=" + player[-1][-4:] + "&team=" + player[-2] + "&nba=true"
        playerJSON = json.loads(requests.get(playerURL).text)

        #Index dictionary to get the per36 stats of the player
        latestPlayerThirtySix = playerJSON["basicPer36"]["nba"]["body"][-1]
        playerInfo.append([float(latestPlayerThirtySix["pts"]), float(latestPlayerThirtySix["reb"]), float(latestPlayerThirtySix["ast"]), 
            float(latestPlayerThirtySix["stl"]), float(latestPlayerThirtySix["blk"]), float(latestPlayerThirtySix["to"])])

        #Index dictionary to get the starter minutes expected for the player
        starterMinutes = playerJSON["splitsStarter"]["nba"]["body"]
        for i in starterMinutes:
            if(i["season"] == ("Starting " + generalizedPosition)):
                playerInfo.append(float(i["minutes"]))
        
        #Add the expected fantasy score of the player to the existing array used in the paramter
        player.append(getFantasyScore(playerInfo[0], playerInfo[1]))

    except:
        player.append(0.0)
        pass

    #Dont want to spam requests to rotowire, will wait 2 seconds between requests
    time.sleep(2)
    

#Merge sort algorithm to sort players by weight, code taken from: https://www.geeksforgeeks.org/merge-sort/
def playerMergeSort(playerArray):
    if len(playerArray) > 1:

        #Middle of the array
        mid = len(playerArray) // 2

        #Left side of the Array (not including middle value)
        left = playerArray[:mid]

        #Right side fo the Array (including middle value)
        right = playerArray[mid:]

        #Sort left side
        playerMergeSort(left)

        #Sort right side
        playerMergeSort(right)

        i = j = k = 0

        #Move data to left and right arrays
        while i < len(left) and j < len(right):
            if(left[i][-1] < right[i][-1]):
                playerArray[k] = left[i]
                i += 1
            else:
                playerArray[k] = right[j]
                j += 1
            k += 1
        
        #Check for missing elements
        while i < len(left):
            playerArray[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            playerArray[k] = right[j]
            j += 1
            k += 1



#Take all players and place their data in an array based on their starting position
def movePlayerToSection(player):
    position = player[1]
    
    if(position == "PG"):
        ALL_PG.append(player)
    elif(position == "SG"):
        ALL_SG.append(player)
    elif(position == "SF"):
        ALL_SF.append(player)
    elif(position == "PF"):
        ALL_PF.append(player)
    else:
        ALL_C.append(player)


##############
# MAIN
##############



#Setup primary array that contains all players guaranteed to start today
getStartingPlayers(STARTING_PLAYERS)

#For each player, add their calculated fantasy score to the end of their personal array
for foundPlayer in STARTING_PLAYERS:
    addScore(foundPlayer)
    #Move the player to an array based on their position
    movePlayerToSection(foundPlayer)

#Sort all position arrays
playerMergeSort(ALL_PG)
playerMergeSort(ALL_SG)
playerMergeSort(ALL_SF)
playerMergeSort(ALL_PF)
playerMergeSort(ALL_C)


#Return top 10 of each position array, all data is sorted from least to greatest
print("Point Guards")
for player in ALL_PG:
    print(player[0], player[1], player[3], player[-1], "\n")

print("Shooting Guards")
for player in ALL_SG:
    print(player[0], player[1], player[3], player[-1], "\n")

print("Small Forwards")
for player in ALL_SF:
    print(player[0], player[1], player[3], player[-1], "\n")

print("Power Forwards")
for player in ALL_PF:
    print(player[0], player[1], player[3], player[-1], "\n")

print("Centers")
for player in ALL_C:
    print(player[0], player[1], player[3], player[-1], "\n")

#TODO: Merge sort doesnt sort correctly, need to have position list ordered in reverse (Greatest to least)