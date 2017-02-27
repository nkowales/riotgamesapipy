import requests

class riotgamesapipy:
 
	def __init__(self, api_key, region = 'na'):
		self.api_key = api_key
		self.region = region

	def getChampions(self, ftp = False):
		if ftp == False:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion?freeToPlay=false&api_key='+ self.api_key)
			
		else:
			r = requests.get('https://' + self.region + '.api.pvp.net/api/lol/' + self.region + '/v1.2/champion?freeToPlay=true&api_key='+ self.api_key)

		champs = r.json()
		return champs
