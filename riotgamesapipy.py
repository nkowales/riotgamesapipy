import requests

class riotgamesapipy:
 
	def __init__(self, api_key, region = 'na'):
		self.api_key = api_key
		self.region = region

	def getChampions(self, ftp = False):
	# all the league champions
		if ftp == False:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion?freeToPlay=false&api_key='+ self.api_key)
			
		else:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion?freeToPlay=true&api_key='+ self.api_key)

		champs = r.json()
		return champs

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
