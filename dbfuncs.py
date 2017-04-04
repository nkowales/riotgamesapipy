import mysql.connector
import info
from id2name import NAME2ID
from id2name import ID2NAME
import riotgamesapipy


#given summoner name return list of champions sorted by that summoner's champion mastery
def getmastery(summname):
	results = []
	rito = riotgamesapipy.riotgamesapipy(info.API_KEY)
	summ = rito.getSummonerbyName(summname)
	for key in summ:
		summid = summ[key]['id']
	masterydata = rito.getPlayerMasteries(str(summid))
	for d in masterydata:
		results.append(d['championId'])
	print results
	return results
		
#given game id, the champion id's for each position, and a 1 or 0 indicating who won, insert data into database
def insertgame(i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w):
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	add_game = ("INSERT INTO games (gameid, top1, top2, jungle1, jungle2, mid1, mid2, bot1, bot2, supp1, supp2, win) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
	game_data = (i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w)
	cursor.execute(add_game, game_data)
	cnx.commit()
	cursor.close()
	cnx.close()

def findbest(position, champid):
	mylist = []
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	#query = ('SELECT COUNT(*) FROM games WHERE ( ' + position + '1 = ' + champid + ' AND ' + position + '2 = ' + enemyid + ' AND win = 1 ) OR ( ' + position + '2 = ' + champid + ' AND ' + position + '1 = ' + enemyid + ' AND win = 0 )')
	query = ('SELECT ' + position + '2, avg(win) AS wr FROM ( ( SELECT gameid, ' + position + '1, ' + position + '2, win FROM games WHERE ' + position + '1 = ' + champid + ' ) UNION ALL ( SELECT gameid, ' + position + '1 AS ' + position + '2, ' + position + '2 AS ' + position + '1, IF( win = 0, 1, 0 ) AS win FROM games WHERE ' + position + '2 = ' + champid + ' ) ) AS z GROUP BY ' + position + '2 HAVING ( COUNT(*) > 29 AND wr > .5 )')
	cursor.execute(query)
	
	for r in cursor:
		mylist.append(r)
	
	cursor.close()
	cnx.close()
	return mylist


#given a position, and 2 champion ids return the number of wins the first champion has against the second
def findwin(position, champid, enemyid):#position same as role, lane assignment. should be top, jungle, mid, bot, or supp
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	query = ('SELECT COUNT(*) FROM games WHERE ( ' + position + '1 = ' + champid + ' AND ' + position + '2 = ' + enemyid + ' AND win = 1 ) OR ( ' + position + '2 = ' + champid + ' AND ' + position + '1 = ' + enemyid + ' AND win = 0 )')
	cursor.execute(query)
	result=cursor.fetchone()
	cursor.close()
	cnx.close()
	return result[0]

#given a position, and 2 champion ids return the number of loses the first champion has against the second
def findlose(position, champid, enemyid):
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	query = ('SELECT COUNT(*) FROM games WHERE ( ' + position + '1 = ' + champid + ' AND ' + position + '2 = ' + enemyid + ' AND win = 0 ) OR ( ' + position + '2 = ' + champid + ' AND ' + position + '1 = ' + enemyid + ' AND win = 1 )')
	cursor.execute(query)
	result=cursor.fetchone()
	cursor.close()
	cnx.close()
	return result[0]

#given a position and a champion id return the wins, loses, winpercentages, and if its a valid sample size(wins + loses > 30)
def findrates(position, champid):
	results = {}
	winsagainst = {}
	losesagainst = {}
	percents = {}
	isvalid = {}
	for key in ID2NAME:
		winsagainst[key] = findwin(position, champid, key)
		losesagainst[key] = findlose(position, champid, key)
		if((winsagainst[key] + losesagainst[key]) > 0):
			percents[key] = ((float(winsagainst[key])/(float(winsagainst[key])+float(losesagainst[key])))*100.0)
		else:
			percents[key] = 0.0
		if((int(winsagainst[key])+int(losesagainst[key])) > 30):
			isvalid[key]=1
		else:
			isvalid[key] = 0
			
	results['wins'] = winsagainst
	results['loses'] = losesagainst
	results['winrates'] = percents
	results['validity'] = isvalid
	return results

#given a champion name, a summoner name, and a position gives suggestions on counter matchup for that summoner
def suggestion(champname, summname, position):
	results = {}
	nsr = []#not sorted results
	champid = NAME2ID[champname]
	temp = findrates(position, champid)
	for key in temp['winrates']:
		if ((temp['winrates'][key]) > 50): #and (temp['validity'][key] == 1)):
			nsr.append(int(key))
	favs = getmastery(summname)
	#print favs
	#print temp['winrates']
	for i in favs:
		if i in nsr:
			results[ID2NAME[str(i)]] = temp['winrates'][str(i)]
	return results
	
		
