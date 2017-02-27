import requests

# SR stands for summoners rift which is the name of the 5x5 map, TT stands for twisted treeline which is the name of the 3x3 map

class riotgamesapipy:
 
	def __init__(self, api_key, region = 'na', server = 'NA1'):
		self.api_key = api_key
		self.region = region
		self.server = server

	### CHAMPION ###
	def getChampions(self, ftp = False):
	# all the league champions
		if ftp == False:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion?freeToPlay=false&api_key='+ self.api_key)
		else:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion?freeToPlay=true&api_key='+ self.api_key)
		champs = r.json()
		return champs
		
	def getChampionByID(self, championID):
	# get champion by champion ID
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion/' + str(championID) + '?api_key='+ self.api_key)
		champ = r.json()
		return champ
		
	### CHAMPION MASTERY ###
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

	### CURRENT GAME ###
	def getCurrentGame(self, summonerID):
	# get the current game by summonerID
		r = requests.get('https://' + self.region + '.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/' + self.server + '/' + str(summonerID) + '?api_key=' + self.api_key)
		cgame = r.json()
		return cgame

	### FEATURED GAMES ###
	def getFeaturedGames(self):
	# get info on the highest ranking current games
		r = requests.get('https://' + self.region + '.api.pvp.net/observer-mode/rest/featured?api_key=' + sefl.api_key)
		fgames = r.json()
		return fgames

	### GAME ###
	def getPlayerRecentGames(self, summonerID):
	# info on a player's recent games
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/na/v1.3/game/by-summoner/' + str(summonerID) + '/recent?api_key=' + self.api_key)
		rgames = r.json()
		return rgames

	### LEAGUES ###
	def getLeagues(self, summonerIDs):
		# get info on the leagues that a given summoner is a member of. Takes
		# comma-separated summoner ids string
		#excludes inactive teams and players except players in the input list
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v2.5/league/by-summoner/' + str(summonerIDs) + '?api_key=' + self.api_key)
		leagues = r.json()
		return leagues

	def getLeagueEntries(self, summonerIDs):
		#gets info on leages summoner is a member of. Takes comma separated string of ids		
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v2.5/league/by-summoner/' + str(summonerIDs) + '/entry?api_key=' + self.api_key)
		leagues = r.json()
		return leagues
		
	def	getChallenger(self, Qname):
		#return challenger league for given ranked queue, RANKED_FLEX_SR, RANKED_FLEX_TT, RANKED_SOLO_5x5, RANKED_TEAM_5x5, or RANKED_TEAM_3x3, 
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v2.5/league/challenger?type=' + Qname + '&api_key=' + self.api_key)
		league = r.json()
		return league
		
	def	getMaster(self, Qname):
		#return Master league for given ranked queue, RANKED_FLEX_SR, RANKED_FLEX_TT, RANKED_SOLO_5x5, RANKED_TEAM_5x5, or RANKED_TEAM_3x3, 
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v2.5/league/master?type=' + Qname + '&api_key=' + self.api_key)
		league = r.json()
		return league
		
	### LoL STATIC DATA ###
	#def getChampionData
	
	def getChampionDataByID(self, championID)
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/champion/' + str(championID) + '?api_key=' + self.api_key)
	
	#def getItemData
	
	#def getItemDataByID
	
	#def getLanguageStrings
	
	#def getLanguages
	
	#def getMapData
	
	#def getMasteryData
	
	#def getMasteryDataByID
	
	#def getRealmData
	
	#def getRuneData
	
	#def getRuneDataByID
	
	#def getSummonerSpellData
	
	#def getSummonerSpellDataByID
	
	#def getVersionData
	
	### LoL STATUS ###
	
	### MATCH ###
	
	### MATCHLIST ###
	
	### STATS ###
	
	### SUMMONER ###
	def getSummonerbyName(self, summonerN):
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.4/summoner/by-name/' + str(summonerN) + '?api_key=' + self.api_key)
		summoner = r.json()
		return summoner

	### PROJECT SPECIFIC ###
