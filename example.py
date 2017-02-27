import riotgamesapipy
from info import API_KEY

def main():
	rito = riotgamesapipy.riotgamesapipy(API_KEY)
	c = rito.getChampions()
	print c

if __name__ == "__main__":
	main()
