import requests

# SR stands for summoners rift which is the name of the 5x5 map, TT stands for twisted treeline which is the name of the 3x3 map

class riotgamesapipy:
 
	def __init__(self, api_key, region = 'na', server = 'NA1', locale = 'en_US'):
		self.api_key = api_key
		self.region = region
		self.server = server
		self.locale = locale


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
		r = requests.get('https://' + self.region + '.api.pvp.net/championmastery/location/' + self.server + '/player/' + str(summonerID) + '/champions?api_key=' + self.api_key)
		masteries = r.json()
		return masteries


	def getChampionMastery(self, summonerID, championID):
	# get summoner's mastery of a given champion, search by summoner and
	# champion IDs
		r = requests.get('https://' + self.region + '.api.pvp.net/championmastery/location/' + self.server + '/player/' + str(summonerID) + '/champion/' + str(championID) + '?api_key=' + self.api_key)
		mastery = r.json()
		return mastery


	def getMasteryScore(self, summonerID):
	# get the total number of summoner mastery points, int
		r = requests.get('https://' + self.region + '.api.pvp.net/championmastery/location/' + self.server + '/player/' + str(summonerID) + '/score?api_key=' + self.api_key)
		score = r.json()
		return int(score)


	def getTopMasteries(self, summonerID, retrieve):
	# get the player's champions w highest masteries
		r = requests.get('https://' + self.region + '.api.pvp.net/championmastery/location/' + self.server + '/player/' + str(summonerID) + '/topchampions?count=' + str(retrieve) + '&api_key=' + self.api_key)
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
	# excludes inactive teams and players except players in the input list
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
	def getChampionData(self):
		r = requests.get('https://global.api.riotgames.com/api/lol/static-data/'+self.region+'/v1.2/champion?locale='+self.locale+'&api_key='+self.api_key)
		champions = r.json()
		return champions
	
	def getChampionDataByID(self, championID):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/champion/' + str(championID) + '?api_key=' + self.api_key)
		champion = r.json()
		return champion
		
	#def getItemData
	def getItemData(self):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/item?itemListData=all&api_key=' + self.api_key)
		items = r.json()
		return items
	
	#def getItemDataByID
	def getItemDataByID(self, itemID):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/item/' + str(itemID) + '?itemData=all&api_key=' + self.api_key)
		item = r.json()
		return item
	
	#def getLanguageStrings

	#def getLanguages
	
	#def getMapData
	def getMapData(self):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/map?api_key=' + self.api_key)
		mapdata = r.json()
		return mapdata
	
	#def getMasteryData
	def getMasteryData(self):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/mastery?api_key=' + self.api_key)
		mastery = r.json()
		return mastery

	#def getMasteryDataByID
	def getMasteryDataByID(self, masteryID):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/mastery/' + str(masteryID) + '?api_key=' + self.api_key)
		mastery = r.json()
		return mastery
	
	#def getRealmData
	def getRealmData(self):
		r - requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/realm?api_key=' + self.api_key)
		realm = r.json()
		return realm

	#def getRuneData
	def getRuneData(self):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + 'v1.2/rune?api_key' + self.api_key)
		rune = r.json()
		return rune
	
	#def getRuneDataByID
	def getRuneDataByID(self, runeID):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + 'v1.2/rune/' + str(runeID) + '?api_key' + self.api_key)
		rune = r.json()
		return rune

	#def getSummonerSpellData
	def getSummonerSpellData(self):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/summoner-spell?api_key=' + self.api_key)
		spell = r.json()
		return spell
	
	#def getSummonerSpellDataByID
	def getSummonerSpellDataByID(self, spellID):
		r = requests.get('https://global.api.pvp.net/api/lol/static-data/' + self.region + '/v1.2/summoner-spell/' + str(spellID) + '?api_key=' + self.api_key)
		spell = r.json()
		return spell
	
	#def getVersionData


	### LoL STATUS ###
	def getShardStatus(self):
		#returns status of shard, or server
		r = requests.get('https://' + self.region + '.api.pvp.net/lol/status/v1/shard?api_key=' + self.api_key)
		shard = r.json()
		return shard
	
	def getShards(self):
		#returns list of shards, or servers
		r = requests.get('https://' + self.region + '.api.pvp.net/lol/status/v1/shards?api_key=' + self.api_key)
		shards = r.json()
		return shards
		

	### MATCH ###
	def getMatch(self, matchID, timeline = False):
		#returns match by match ID, with timeline tag indicating whether to include timeline data or not
		if timeline == True:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v2.2/match/' + str(matchID) + '?includeTimeline=true&api_key=' + self.api_key)
		else:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v2.2/match/' + str(matchID) + '?includeTimeline=false&api_key=' + self.api_key)
		match = r.json()
		return match
	

	### MATCHLIST ###
        def getMatchList(self, summonerID, rankedQueues=None, endTime=None, endIndex=None, beginTime=None, beginIndex=None, seasons=None, championIds=None):
                options=''
                if rankedQueues:
                        options = options + 'rankedQueues=' + str(rankedQueues) + '&'
                if endTime:
                        options = options + 'endTime=' + str(endTime) + '&'
                if endIndex:
                        options = options + 'endIndex=' + str(endIndex) + '&'
                if beginTime:
                        options = options + 'beginTime=' + str(beginTime) + '&'
                if beginIndex:
                        options = options + 'beginIndex=' + str(beginIndex) + '&'
                if seasons:
                        options = options + 'seasons=' + str(seasons) + '&'
                if championIds:
                        options = options + 'championIds=' + str(championIds) + '&'
                
                r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v2.2/matchlist/by-summoner/' + str(summonerID) + '?' + options + 'api_key=' + self.api_key)
                matchlist = r.json()
                return matchlist

		
	### STATS ###
	def getRankedStats(self, summonerID, season):
		#seasons include SEASON2017, SEASON2016, SEASON2015, SEASON2014, and SEASON3
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.3/stats/by-summoner/'+ summonerID + '/ranked?season=' + season + '&api_key=' + self.api_key)
		stats = r.json()
		return stats
	
	def getStatsSummary(self, summonerID, season):
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.3/stats/by-summoner/'+ summonerID + '/summary?season=' + season + '&api_key=' + self.api_key)
		stats = r.json()
		return stats

	
	### SUMMONER ###
	def getSummonerbyName(self, summonerN):
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.4/summoner/by-name/' + str(summonerN) + '?api_key=' + self.api_key)
		summoner = r.json()
		return summoner
		
	def getSummonersByID(self, summonerIDs):
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.4/summoner/' + str(summonerID) + '?api_key=' + self.api_key)
		summoners = r.json()
		return summoners 

	def getSummonersByAcctID(self, accountIDs):
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.4/summoner/by-account/' + str(accountID) +'?api_key=' + self.api_key)
		summoners = r.json()
		return summoners 

	def getSummonerNameByID(self, summonerID):
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.4/summoner/' + str(summonerID) + '/name?api_key=' + self.api_key)
		name = r.json()
		return name

	def getSummonersMasteries(self, summonerIDs):
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.4/summoner/' + str(summonerIDs) + '/masteries?api_key=' + self.api_key)
		masteries = r.json()
		return masteries

	def getSummonersRunes(self, summonerID):
		r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.4/summoner/' + str(summonerIDs) + '/runes?api_key=' + self.api_key)
		runes = r.json()
		return runes

	### PROJECT SPECIFIC ###
