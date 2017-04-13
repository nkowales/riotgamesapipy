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
		results.append((d['championId'], d["championPoints"]))
	#print results
	return results
		
#given game id, the champion id's for each position, and a 1 or 0 indicating who won, insert data into database
def insertgame(i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w, r):
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	add_game = ("INSERT INTO games (gameid, top1, top2, jungle1, jungle2, mid1, mid2, bot1, bot2, supp1, supp2, win, rank) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
	game_data = (i, t1, t2, j1, j2, m1, m2, b1, b2, s1, s2, w, r)
	cursor.execute(add_game, game_data)
	cnx.commit()
	cursor.close()
	cnx.close()

def findbest(position, champid):
	myd = {}
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	#query = ('SELECT COUNT(*) FROM games WHERE ( ' + position + '1 = ' + champid + ' AND ' + position + '2 = ' + enemyid + ' AND win = 1 ) OR ( ' + position + '2 = ' + champid + ' AND ' + position + '1 = ' + enemyid + ' AND win = 0 )')
	#SELECT pos2, AVG(w) as wr FROM ( ( SELECT gameid, top2 AS pos1, top1 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE top2 = 154 ) UNION ALL ( SELECT gameid, top1 AS pos1, top2 AS pos2, win AS w FROM games WHERE top1 = 154 ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC;
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, ' + position + '2 AS pos1, ' + position + '1 AS pos2, IF( win = 0, 1, 0) AS w FROM games WHERE ' + position + '2 = ' + champid + ' ) UNION ALL ( SELECT gameid, ' + position + '1 AS pos1, ' + position + '2 AS pos2, win AS w FROM games WHERE ' + position + '1 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	
	cursor.close()
	cnx.close()
	return myd


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
	results = []
	#nsr = []#not sorted results
	champid = NAME2ID[champname]
	temp = findbest(position, champid)
	favs = getmastery(summname)
	for i in favs:
		if i[0] in temp:
			results.append((ID2NAME[str(i[0])], i[1], temp[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results
	
		
