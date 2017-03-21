import mysql.connector
import info
from id2name import NAME2ID
from id2name import ID2NAME

winsagainst = {}
losesagainst = {}

def insertgame(i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w):

	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	add_game = ("INSERT INTO games (gameid, top1, top2, jungle1, jungle2, mid1, mid2, bot1, bot2, supp1, supp2, win) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
	game_data = (i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w)
	cursor.execute(add_game, game_data)
	cnx.commit()
	cursor.close()
	cnx.close()

def findwins(position, champid):
	winsagainst = {}
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	query = ('SELECT COUNT(*) FROM games WHERE ( ' + position + '1 = ' + champid + ' AND win = 1 ) OR (' + position + '2 = ' + champid + ' AND win = 0 )')
	cursor.execute(query)
	result=cursor.fetchone()
	cursor.close()
	cnx.close()
	return result[0]
