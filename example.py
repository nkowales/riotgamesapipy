import riotgamesapipy
from info import API_KEY

def main():
	rito = riotgamesapipy.riotgamesapipy(API_KEY)
	c = rito.getChampionMastery(43103897, 36)
	print c

if __name__ == "__main__":
	main()