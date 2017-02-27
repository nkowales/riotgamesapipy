import riotgamesapipy
from info import API_KEY

def main():
	rito = riotgamesapipy.riotgamesapipy(API_KEY)
	c = rito.getSummonerbyName('Dairus')
	print "Looking up stats for player 'Dairus', ID:", c["dairus"]["id"]

if __name__ == "__main__":
	main()
