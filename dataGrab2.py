import riotgamesapipy
import time
from info import API_KEY
import dbfuncs


def main():
	rito = riotgamesapipy.riotgamesapipy(API_KEY)
	DESIREDSEASON1 = 'SEASON2017'
	DESIREDSEASON2 = 'PRESEASON2017'
	matches=[] # list of games we got info from

	# for non-challenger entries - 
	#bronzechamp = rito.getLeagues(39153354)
	#bronze = bronzechamp["39153354"][0]
	#silverchamp = rito.getLeagues(51575588)
	#silver = silverchamp["51575588"][0]
	#goldchamp = rito.getLeagues(35707215)
	#gold = goldchamp["35707215"][0]
	#platinumchamp = rito.getLeagues(31593648)
	#platinum = platinumchamp["31593648"][0]
	
	master = rito.getMaster('RANKED_SOLO_5x5')
	#challenger = rito.getChallenger('RANKED_SOLO_5x5')
	
	attempt = 0
	for entry in master["entries"]: # replace "challenger" with other league
		matchlist = rito.getMatchList(str(entry["playerOrTeamId"]))
		time.sleep(1)
		if 'matches' in matchlist:
			for matl in matchlist["matches"]:
				try:
					if ((matl['season'] == DESIREDSEASON1) or (matl['season'] == DESIREDSEASON2)):
						attempt += 1
						matchID = matl["matchId"]
						role = [None] * 10
						if matchID not in matches:
							time.sleep(1)
							matches.append(matchID)
							match = rito.getMatch(matchID, timeline=True)
							for part in match["participants"]:
								if part["timeline"]["lane"] == "BOTTOM" and part["timeline"]["role"] == "DUO_CARRY":
									if part["teamId"] == 100:
										role[6] = str(part["championId"])
									else:
										role[7] = str(part["championId"])
								elif part["timeline"]["lane"] == "BOTTOM" and part["timeline"]["role"] == "DUO_SUPPORT":
									if part["teamId"] == 100:
										role[8] = str(part["championId"])
									else:
										role[9] = str(part["championId"])
								elif part["timeline"]["lane"] == "TOP":
									if part["teamId"] == 100:
										role[0] = str(part["championId"])
									else:
										role[1] = str(part["championId"])
								elif part["timeline"]["lane"] == "JUNGLE":
									if part["teamId"] == 100:
										role[2] = str(part["championId"])
									else:
										role[3] = str(part["championId"])
								elif part["timeline"]["lane"] == "MIDDLE":
									if part["teamId"] == 100:
										role[4] = str(part["championId"])
									else:
										role[5] = str(part["championId"])
							if match["teams"][0]["winner"]:
								w="1"
							else:
								w="0"
				
							dbfuncs.insertgame(matchID, role[0], role[1], role[2], role[3], role[4], role[5], role[6], role[7], role[8], role[9], w, 'mc')
							#dbfuncs.insertgame(matchID, top1, top2, jun1, jun2, mid1, mid2, bot1, bot2, sup1, sup2, w)
				except Exception as e:
					try: 
						print 'Attempt number ' + str(attempt) + ': Error ' + matchlist['status']['status_code'] + ': ' +  matchlist['status']['message']
					except:
						print 'Attempt number ' + str(attempt) + ': ' + str(e)
				
		else:
			print 'No matches found'

if __name__ == "__main__":
        main()
