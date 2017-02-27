import riotgamesapipy
from info import API_KEY

def main():
	rito = riotgamesapipy.riotgamesapipy(API_KEY)
	c = rito.getSummonerbyName('Dairus')
	print "Looking up stats for player 'Dairus', ID:", c["dairus"]["id"]

	idnum = c["dairus"]["id"]
	league = rito.getLeagueEntries(idnum)
	#print league[str(c["dairus"]["id"])]
	print "Tier:", league[str(idnum)][0]["tier"], league[str(idnum)][0]["entries"][0]["division"]
	print "Wins / Losses: ", league[str(idnum)][0]["entries"][0]["wins"], "/", league[str(idnum)][0]["entries"][0]["losses"]

if __name__ == "__main__":
	main()
