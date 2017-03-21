import mysql.connector
from info import USER
from info import PASSWORD
from info import HOST

def insertgame(i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w)

	cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database='lol')
	cursor = cnx.cursor()
	add_game = ("INSERT INTO games (id, top1, top2, jungle1, jungle2, mid1, mid2, bot1, bot2, supp1, supp2, win) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
	game_data = (i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w)
	cursor.execute(add_game, game_data)
	cnx.commit()
	cursor.close()
	cnx.close()


