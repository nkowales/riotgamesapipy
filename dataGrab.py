import riotgamesapipy
from info import API_KEY

def main():
        rito = riotgamesapipy.riotgamesapipy(API_KEY)

	matches=[] # list of games we got info from

	# for non-challenger entries - 
	bronzechamp = rito.getLeagues(37517949)
	bronze = bronzechamp["37517949"][0]
	silverchamp = rito.getLeagues(51575588)
	silver = silverchamp["51575588"][0]
	goldchamp = rito.getLeagues(35707215)
	gold = goldchamp["35707215"][0]
	platinumchamp = rito.getLeagues(31593648)
	platinum = platinumchamp["31593648"][0]

	master = rito.getMaster('RANKED_SOLO_5x5')
	challenger = rito.getChallenger('RANKED_SOLO_5x5')

        for entry in platinum["entries"]: # replace "challenger" with other league
                matchlist = rito.getMatchList(str(entry["playerOrTeamId"]), seasons='SEASON2016,PRESEASON2017')
                for matl in matchlist["matches"]:
                        matchID = matl["matchId"]
			if matchID not in matches:
				matches.append(matchID)
				print matchID
                        	match = rito.getMatch(matchID, timeline=True)
	                        for part in match["participants"]:
			#		grabStats(rito, part)
					champ = rito.getChampionDataByID(part["championId"])
					if part["timeline"]["lane"] == "BOTTOM" and part["timeline"]["role"] == "DUO_CARRY":
				                role = "ADCARRY"
					elif part["timeline"]["lane"] == "BOTTOM" and part["timeline"]["role"] == "DUO_SUPPORT":
                				role = "SUPPORT"
				        else:
                				role = part["timeline"]["lane"]
					print role, champ["name"], part["stats"]["winner"]
                                
					# rival champ stats!
                        		#for part2 in match["participants"]:
                                	#	if part["timeline"]["lane"] == part2["timeline"]["lane"] and part["timeline"]["role"] == part2["timeline"]["role"] and part["participantId"] != part2["participantId"]:
                                        #	        print "Rival Stats!!"
                                         #       	grabStats(rito, part2)
                



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
        print part["stats"]["totalHeal"] # i assume healing others? healing done to allies, including self, excluding health regeneration and lifesteal


if __name__ == "__main__":
        main()
