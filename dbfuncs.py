import mysql.connector
from info import USER
from info import PASSWORD
from info import HOST
from id2name import NAME2ID
from id2name import ID2NAME


def insertgame(i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w):

	cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database='lol')
	cursor = cnx.cursor()
	add_game = ("INSERT INTO games (gameid, top1, top2, jungle1, jungle2, mid1, mid2, bot1, bot2, supp1, supp2, win) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
	game_data = (i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w)
	cursor.execute(add_game, game_data)
	cnx.commit()
	cursor.close()
	cnx.close()

def findmatchups(position, champid):

	cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database='lol')
	cursor = cnx.cursor()
	query = ('SELECT * FROM games')
	#data = (position, champid)
	stuff =[]
	cursor.execute(query)
	for (gameid, top1, top2, jungle1, jungle2, mid1, mid2, bot1, bot2, supp1, supp2, win) in cursor:
		stuff.append(gameid)
	cursor.close()
	cnx.close()
	return stuff
