import mysql.connector
import info
from id2name import NAME2ID
from id2name import ID2NAME



def insertgame(i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w):

	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	add_game = ("INSERT INTO games (gameid, top1, top2, jungle1, jungle2, mid1, mid2, bot1, bot2, supp1, supp2, win) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
	game_data = (i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w)
	cursor.execute(add_game, game_data)
	cnx.commit()
	cursor.close()
	cnx.close()

def findwin(position, champid, enemyid):#position same as role, lane assignment. should be top, jungle, mid, bot, or supp
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	query = ('SELECT COUNT(*) FROM games WHERE ( ' + position + '1 = ' + champid + ' AND ' + position + '2 = ' + enemyid + ' AND win = 1 ) OR ( ' + position + '2 = ' + champid + ' AND ' + position + '1 = ' + enemyid + ' AND win = 0 )')
	cursor.execute(query)
	result=cursor.fetchone()
	cursor.close()
	cnx.close()
	return result[0]

def findlose(position, champid, enemyid):
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	query = ('SELECT COUNT(*) FROM games WHERE ( ' + position + '1 = ' + champid + ' AND ' + position + '2 = ' + enemyid + ' AND win = 0 ) OR ( ' + position + '2 = ' + champid + ' AND ' + position + '1 = ' + enemyid + ' AND win = 1 )')
	cursor.execute(query)
	result=cursor.fetchone()
	cursor.close()
	cnx.close()
	return result[0]


def findrates(position, champid):
	results = {}
	winsagainst = {}
	losesagainst = {}
	percents = {}
	isvalid = {}
	for key in ID2NAME:
		winsagainst[key] = findwin(position, champid, key)
		losesagainst[key] = findlose(position, champid, key)
		percents[key] = ((float(winsagainst[key])/(float(winsagainst[key])+float(losesagainst[key])))*100.0)
		if((int(winsagainst[key])+int(losesagainst[key])) > 30):
			isvalid[key]=1
		else:
			isvalid[key] = 0
			
	results['wins'] = winsagainst
	results['loses'] = losesagainst
	results['winrates'] = percents
	results['validity'] = isvalid
	return results


		
