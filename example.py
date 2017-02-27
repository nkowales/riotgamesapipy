import riotgamesapipy
from info import API_KEY

def main():
	rito = riotgamesapipy.riotgamesapipy(API_KEY)
	c = rito.getSummonerbyName('Dyrus')
	print "Looking up stats for player 'Dyrus', ID:", c["dyrus"]["id"]

	idnum = c["dyrus"]["id"]
	league = rito.getLeagueEntries(idnum)
	#print league[str(c["dyrus"]["id"])]
	print "Tier:", league[str(idnum)][0]["tier"], league[str(idnum)][0]["entries"][0]["division"]
	print "Wins / Losses: ", league[str(idnum)][0]["entries"][0]["wins"], "/", league[str(idnum)][0]["entries"][0]["losses"]
	
	masteries = rito.getTopMasteries(str(idnum), 10)
	print "Dyrus' Top 10 Masteries:"
	for entry in masteries:
		champ = rito.getChampionDataByID(entry["championId"])
		print "Name:", champ["name"], "\t\t", "Level:", entry["championLevel"], "\t", "Points towards Mastery:", entry["championPoints"]
	#irint masteries

if __name__ == "__main__":
	main()
