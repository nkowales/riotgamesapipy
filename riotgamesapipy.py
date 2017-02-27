import requests

class riotgamesapipy:
 
	def __init__(self, api_key, region = 'na', server = 'NA1'):
		self.api_key = api_key
		self.region = region
		self.server = server

	def getChampions(self, ftp = False):
	# all the league champions
		if ftp == False:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion?freeToPlay=false&api_key='+ self.api_key)
			
		else:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion?freeToPlay=true&api_key='+ self.api_key)

		champs = r.json()
		return champs

	def getCurrentGame(self, summonerID):
		r = requests.get('https://' + self.region + '.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/' + self.server + '/' + str(summonerID) + '?api_key=' + self.api_key)
		cgame = r.json()
		return cgame
		
	def getChampionByID(self, championID):
		# champion by champion ID
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion/' + str(championID) + '?api_key='+ self.api_key)
		champ = r.json()
		return champ
		
	def getPlayerMasteries(self, summonerID):
	# get that summoner's champion masteries, search by ID
		r = requests.get('https://' + self.region + '.api.pvp.net/championmastery/location/' + self.region + '1/player/' + str(summonerID) + '/champions?api_key=' + self.api_key)
		masteries = r.json()
		return masteries

	def getChampionMastery(self, summonerID, championID):
	# get summoner's mastery of a given champion, search by summoner and
	# champion IDs
		r = requests.get('https://' + self.region + '.api.pvp.net/championmastery/location/' + self.region + '1/player/' + str(summonerID) + '/champion/' + str(championID) + '?api_key=' + self.api_key)
		mastery = r.json()
		return mastery

	def getMasteryScore(self, summonerID):
	# get the total number of summoner mastery points, int
		r = requests.get('https://' + self.region + '.api.pvp.net/championmastery/location/' + self.region + '1/player/' + str(summonerID) + '/score?api_key=' + self.api_key)
		score = r.json()
		return int(score)

	def getTopMasteries(self, summonerID, retrieve):
	# get the player's champions w highest masteries
		r = requests.get('https://' + self.region + '.api.pvp.net/championmastery/location/' + self.region + '1/player/' + str(summonerID) + '/topchampions?count=' + str(retrieve) + '&api_key=' + self.api_key)
		top = r.json()
		return top

	def getFeaturedGames(self):
	# get info on the highest ranking current games
		r = requests.get('https://' + self.region + '.api.pvp.net/observer-mode/rest/featured?api_key=' + sefl.api_key)
		fgames = r.json()
		return fgames

	def getPlayerRecentGames(self, summonerID):
	# info on a player's recent games
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/na/v1.3/game/by-summoner/' + str(summonerID) + '/recent?api_key=' + self.api_key)
		rgames = r.json()
		return rgames
