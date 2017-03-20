import riotgamesapipy
from info import API_KEY

def main():
        rito = riotgamesapipy.riotgamesapipy(API_KEY)

	# for non-challenger entries - 
	# gotta find a player in other leagues
	silverchamp = rito.getLeagues(51575588)
	silver = silverchamp["51575588"][0]

	challenger = rito.getChallenger('RANKED_SOLO_5x5')
        for entry in challenger["entries"]: # replace "challenger" with other league
                matchlist = rito.getMatchList(str(entry["playerOrTeamId"]), seasons='SEASON2016,PRESEASON2017')
                for matl in matchlist["matches"]:
                        matchID = matl["matchId"]
                        match = rito.getMatch(matchID, timeline=True)
                        for part in match["participants"]:
                                grabStats(rito, part)
                                
                                # rival champ stats!
                                for part2 in match["participants"]:
                                        if part["timeline"]["lane"] == part2["timeline"]["lane"] and part["timeline"]["role"] == part2["timeline"]["role"] and part["participantId"] != part2["participantId"]:
                                                print "Rival Stats!!"
                                                grabStats(rito, part2)
                        
                
def grabStats(rito, part):
        champ = rito.getChampionDataByID(part["championId"])
        print champ["name"]
        # get the champion's role
        if part["timeline"]["lane"] == "BOTTOM" and part["timeline"]["role"] == "DUO_CARRY":
                print "ADCARRY"
        elif part["timeline"]["lane"] == "BOTTOM" and part["timeline"]["role"] == "DUO_SUPPORT":
                print "SUPPORT"
        else:
                print part["timeline"]["lane"]
        # get some general statistics for that champion
        # lots of good stuff under "timeline" (e.g. gold diff, cs diff)
        # but i'm leaving that out for right now.
        print part["stats"]["winner"]
        print part["stats"]["kills"]
        print part["stats"]["assists"]
        print part["stats"]["deaths"]
        print part["stats"]["physicalDamageDealt"]
        print part["stats"]["magicDamageDealt"]
        print part["stats"]["goldEarned"]
        print part["stats"]["totalDamageTaken"]
        print part["stats"]["totalHeal"] # i assume healing others?


####### dyrus example that we showed the prof #######

#	print "Looking up stats for player 'Dyrus', ID:", c["dyrus"]["id"]

#	idnum = c["dyrus"]["id"]
#	league = rito.getLeagueEntries(idnum)
	#print league[str(c["dyrus"]["id"])]
#	print "Tier:", league[str(idnum)][0]["tier"], league[str(idnum)][0]["entries"][0]["division"]
#	print "Wins / Losses: ", league[str(idnum)][0]["entries"][0]["wins"], "/", league[str(idnum)][0]["entries"][0]["losses"]
	
#	masteries = rito.getTopMasteries(str(idnum), 10)
#	print "Dyrus' Top 10 Masteries:"
#	for entry in masteries:
#		champ = rito.getChampionDataByID(entry["championId"])
#		print "Name:", champ["name"], "\t\t", "Level:", entry["championLevel"], "\t", "Points towards Mastery:", entry["championPoints"]
	#irint masteries

if __name__ == "__main__":
        main()
