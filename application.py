from flask import Flask, render_template, json, request, redirect
from flask.ext.mysql import MySQL
from id2name import NAME2ID
from id2name import ID2NAME
from nicknames2names import NICKNAMES2NAMES
import info
import riotgamesapipy

pos = ['supp', 'bot', 'mid', 'jungle', 'top']#valid position entries
posnn = {'support' : 'supp', 'sup' : 'supp', 'adc' : 'bot', 'bottom' : 'bot', 'middle' : 'mid', 'solomid' : 'mid', 'jung' : 'jungle', 'jun' : 'jungle', 'j' : 'jungle'}#common alternate position names


application = Flask(__name__)
mysql = MySQL()

 
# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = info.USER
application.config['MYSQL_DATABASE_PASSWORD'] = info.PASSWORD
application.config['MYSQL_DATABASE_DB'] = info.DATABASE
application.config['MYSQL_DATABASE_HOST'] = info.HOST
mysql.init_app(application)



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

#given position and champion give winning matchups
def findbest(position, champid):
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	#query = ('SELECT COUNT(*) FROM games WHERE ( ' + position + '1 = ' + champid + ' AND ' + position + '2 = ' + enemyid + ' AND win = 1 ) OR ( ' + position + '2 = ' + champid + ' AND ' + position + '1 = ' + enemyid + ' AND win = 0 )')
	#SELECT pos2, AVG(w) as wr FROM ( ( SELECT gameid, top2 AS pos1, top1 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE top2 = 154 ) UNION ALL ( SELECT gameid, top1 AS pos1, top2 AS pos2, win AS w FROM games WHERE top1 = 154 ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC;
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, ' + position + '2 AS pos1, ' + position + '1 AS pos2, win AS w FROM games WHERE ' + position + '2 = ' + champid + ' ) UNION ALL ( SELECT gameid, ' + position + '1 AS pos1, ' + position + '2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE ' + position + '1 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	
	cursor.close()
	cnx.close()
	return myd

#given position and champion id give top matchups
def findbestavailable(position, champid):
	myd = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, ' + position + '2 AS pos1, ' + position + '1 AS pos2, win AS w FROM games WHERE ' + position + '2 = ' + champid + ' ) UNION ALL ( SELECT gameid, ' + position + '1 AS pos1, ' + position + '2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE ' + position + '1 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	
	for (i, w) in cursor:
		myd.append((ID2NAME[str(i)],w))
	
	cursor.close()
	cnx.close()
	return myd

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
	
	
#given championgive good matchups.
def findlook(champname, position):
	champid = NAME2ID[champname]
	myd = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, ' + position + '2 AS pos1, ' + position + '1 AS pos2, win AS w FROM games WHERE ' + position + '2 = ' + champid + ' ) UNION ALL ( SELECT gameid, ' + position + '1 AS pos1, ' + position + '2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE ' + position + '1 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr ASC LIMIT 20')
	cursor.execute(query)
	
	for (i, w) in cursor:
		myd.append((ID2NAME[str(i)],w))
	
	cursor.close()
	cnx.close()
	return myd

#given enemy bot laner suggest support pick
def findsvb(sname, champname):
	results = []
	champid = NAME2ID[champname]
	
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, bot2 AS pos1, supp1 AS pos2, win AS w FROM games WHERE bot2 = ' + champid + ' ) UNION ALL ( SELECT gameid, bot1 AS pos1, supp2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE bot1 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	cursor.close()
	cnx.close()
	
	favs = getmastery(sname)
	for i in favs:
		if i[0] in myd:
			results.append((ID2NAME[str(i[0])], i[1], myd[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results

#given enemy bot laner suggest support pick
def findsvbavailable(champname):
	results = []
	champid = NAME2ID[champname]
	myl = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, bot2 AS pos1, supp1 AS pos2, win AS w FROM games WHERE bot2 = ' + champid + ' ) UNION ALL ( SELECT gameid, bot1 AS pos1, supp2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE bot1 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl

#given enemy support suggest bot lane pick
def findbvs(sname, champname):
	results = []
	champid = NAME2ID[champname]
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, supp2 AS pos1, bot1 AS pos2, win AS w FROM games WHERE supp2 = ' + champid + ' ) UNION ALL ( SELECT gameid, supp1 AS pos1, bot2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE supp1 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	cursor.close()
	cnx.close()
	
	favs = getmastery(sname)
	for i in favs:
		if i[0] in myd:
			results.append((ID2NAME[str(i[0])], i[1], myd[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results

#given enemy support suggest bot lane pick
def findbvsavailable(champname):
	results = []
	champid = NAME2ID[champname]
	myl = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, supp2 AS pos1, bot1 AS pos2, win AS w FROM games WHERE supp2 = ' + champid + ' ) UNION ALL ( SELECT gameid, supp1 AS pos1, bot2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE supp1 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl

#given your support suggest bot lane pick
def findbws(sname, champname):
	results = []
	champid = NAME2ID[champname]
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, supp1 AS pos1, bot1 AS pos2, win AS w FROM games WHERE supp1 = ' + champid + ' ) UNION ALL ( SELECT gameid, supp2 AS pos1, bot2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE supp2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	cursor.close()
	cnx.close()
	
	favs = getmastery(sname)
	for i in favs:
		if i[0] in myd:
			results.append((ID2NAME[str(i[0])], i[1], myd[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results

#given your support suggest bot lane pick
def findbwsavailable(champname):
	results = []
	champid = NAME2ID[champname]
	myl = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, supp1 AS pos1, bot1 AS pos2, win AS w FROM games WHERE supp1 = ' + champid + ' ) UNION ALL ( SELECT gameid, supp2 AS pos1, bot2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE supp2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl

#given your support suggest bot lane pick
def findswb(sname, champname):
	results = []
	champid = NAME2ID[champname]
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, bot1 AS pos1, supp1 AS pos2, win AS w FROM games WHERE bot1 = ' + champid + ' ) UNION ALL ( SELECT gameid, bot2 AS pos1, supp2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE bot2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	cursor.close()
	cnx.close()
	
	favs = getmastery(sname)
	for i in favs:
		if i[0] in myd:
			results.append((ID2NAME[str(i[0])], i[1], myd[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results

#given your support suggest bot lane pick
def findswbavailable(champname):
	results = []
	champid = NAME2ID[champname]
	myl = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, bot1 AS pos1, supp1 AS pos2, win AS w FROM games WHERE bot1 = ' + champid + ' ) UNION ALL ( SELECT gameid, bot2 AS pos1, supp2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE bot2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl

#given your middle suggest jungle pick
def findjwm(sname, champname):
	results = []
	champid = NAME2ID[champname]
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, mid1 AS pos1, jungle1 AS pos2, win AS w FROM games WHERE mid1 = ' + champid + ' ) UNION ALL ( SELECT gameid, mid2 AS pos1, jungle2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE mid2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	cursor.close()
	cnx.close()
	
	favs = getmastery(sname)
	for i in favs:
		if i[0] in myd:
			results.append((ID2NAME[str(i[0])], i[1], myd[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results

#given your middle suggest jungle pick
def findjwmavailable(champname):
	results = []
	champid = NAME2ID[champname]
	myl = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, mid1 AS pos1, jungle1 AS pos2, win AS w FROM games WHERE mid1 = ' + champid + ' ) UNION ALL ( SELECT gameid, mid2 AS pos1, jungle2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE mid2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl

#given your jungle suggest mid pick
def findmwj(sname, champname):
	results = []
	champid = NAME2ID[champname]
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, jungle1 AS pos1, mid1 AS pos2, win AS w FROM games WHERE jungle1 = ' + champid + ' ) UNION ALL ( SELECT gameid, jungle2 AS pos1, mid2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE jungle2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	cursor.close()
	cnx.close()
	
	favs = getmastery(sname)
	for i in favs:
		if i[0] in myd:
			results.append((ID2NAME[str(i[0])], i[1], myd[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results

#given your jungle suggest mid pick
def findmwjavailable(champname):
	results = []
	champid = NAME2ID[champname]
	myl = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, jungle1 AS pos1, mid1 AS pos2, win AS w FROM games WHERE jungle1 = ' + champid + ' ) UNION ALL ( SELECT gameid, jungle2 AS pos1, mid2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE jungle2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl

#given your top suggest jungle pick
def findjwt(sname, champname):
	results = []
	champid = NAME2ID[champname]
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, top1 AS pos1, jungle1 AS pos2, win AS w FROM games WHERE top1 = ' + champid + ' ) UNION ALL ( SELECT gameid, top2 AS pos1, jungle2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE top2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	cursor.close()
	cnx.close()
	
	favs = getmastery(sname)
	for i in favs:
		if i[0] in myd:
			results.append((ID2NAME[str(i[0])], i[1], myd[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results

#given your jungle suggest top pick
def findtwj(sname, champname):
	results = []
	champid = NAME2ID[champname]
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, jungle1 AS pos1, top1 AS pos2, win AS w FROM games WHERE jungle1 = ' + champid + ' ) UNION ALL ( SELECT gameid, jungle2 AS pos1, top2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE jungle2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	cursor.close()
	cnx.close()
	
	favs = getmastery(sname)
	for i in favs:
		if i[0] in myd:
			results.append((ID2NAME[str(i[0])], i[1], myd[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results

#given your jungle suggest top pick
def findtwjavailable(champname):
	results = []
	champid = NAME2ID[champname]
	myl = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, jungle1 AS pos1, top1 AS pos2, win AS w FROM games WHERE jungle1 = ' + champid + ' ) UNION ALL ( SELECT gameid, jungle2 AS pos1, top2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE jungle2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl

#given your top suggest jungle pick
def findjwtavailable(champname):
	results = []
	champid = NAME2ID[champname]
	myl = []
	cnx = mysql.connector.connect(user=info.USER, password=info.PASSWORD, host=info.HOST, database=info.DATABASE, port=info.PORT)
	cursor = cnx.cursor()
	query = ('SELECT pos2, AVG(w) AS wr FROM ( ( SELECT gameid, top1 AS pos1, jungle1 AS pos2, win AS w FROM games WHERE top1 = ' + champid + ' ) UNION ALL ( SELECT gameid, top2 AS pos1, jungle2 AS pos2, IF( win = 0, 1, 0 ) AS w FROM games WHERE top2 = ' + champid + ' ) ) AS z GROUP BY pos2 HAVING COUNT(*) > 30 ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl

#basic blind pick suggestions by win rate
def findbasicblind(sname, position):
	results = []
	myd = {}
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos, AVG(w) AS wr FROM ( ( SELECT ' + position + '1 AS pos, win AS w FROM games ) UNION ALL ( SELECT ' + position + '2 AS pos, IF( win = 0, 1, 0 ) AS w FROM games ) ) AS z GROUP BY pos HAVING COUNT(*) > 30 AND wr > .5 ORDER BY wr DESC')
	cursor.execute(query)
	for (i, w) in cursor:
		myd[int(i)] = float(w)
	cursor.close()
	cnx.close()
	
	favs = getmastery(sname)
	for i in favs:
		if i[0] in myd:
			results.append((ID2NAME[str(i[0])], i[1], myd[i[0]]))
			results.sort(key=lambda tup: tup[1], reverse=True)
	return results

#basic blind pick suggestions by win rate
def findbasicblindavailable(champname):
	results = []
	champid = NAME2ID[champname]
	myl = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos, AVG(w) AS wr FROM ( ( SELECT ' + position + '1 AS pos, win AS w FROM games ) UNION ALL ( SELECT ' + position + '2 AS pos, IF( win = 0, 1, 0 ) AS w FROM games ) ) AS z GROUP BY pos HAVING COUNT(*) > 30 AND ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl

#find highest win rates to use to suggest bans
def findbans():
	results = []
	myl = []
	cnx = mysql.connect()
	cursor = cnx.cursor()
	query = ('SELECT pos, AVG(w) AS wr FROM ( ( SELECT top1 AS pos, win AS w FROM games ) UNION ALL ( SELECT jungle1 AS pos, win AS w FROM games ) UNION ALL ( SELECT mid1 AS pos, win AS w FROM games ) UNION ALL ( SELECT bot1 AS pos, win AS w FROM games )  UNION ALL ( SELECT supp1 AS pos, win AS w FROM games ) UNION ALL ( SELECT top2 AS pos, IF( win = 0, 1, 0 ) AS w FROM games ) UNION ALL ( SELECT jungle2 AS pos, IF( win = 0, 1, 0 ) AS w FROM games ) UNION ALL ( SELECT mid2 AS pos, IF( win = 0, 1, 0 ) AS w FROM games ) UNION ALL ( SELECT bot2 AS pos, IF( win = 0, 1, 0 ) AS w FROM games ) UNION ALL ( SELECT supp2 AS pos, IF( win = 0, 1, 0 ) AS w FROM games ) ) AS z GROUP BY pos ORDER BY wr DESC LIMIT 20')
	cursor.execute(query)
	for (i, w) in cursor:
		myl.append((ID2NAME[str(i)],w))
	cursor.close()
	cnx.close()
	return myl



@application.route("/")
def main():
	return render_template('index.html')

@application.route('/showBasic')
def showBasic():
	return render_template('basicsuggestion.html')

@application.route('/lookup')
def lookup():
	return render_template('lookup.html')
	
@application.route('/svb')
def supportvsbottom():
	return render_template('suppvbot.html')
	
@application.route('/bvs')
def bottomvssupport():
	return render_template('botvsupp.html')
	
@application.route('/bans')
def suggestbans():
	results = findbans()
	mystr = ''
	for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
	return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Suggested Bans</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 

@application.route('/bws')
def bottomwithsupport():
	return render_template('botwsupp.html')
	
@application.route('/bwsr',methods=['POST'])
def bottomwwithsupportresults():
	_name = request.form['inputName']
	_champ = request.form['inputChamp']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		results = findbws(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = findbwsavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/bws">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Suggested Bottom Laners for that Support</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@application.route('/swb')
def supportwithbottom():
	return render_template('suppwbot.html')
	
@application.route('/swbr',methods=['POST'])
def supportwithbottomresults():
	_name = request.form['inputName']
	_champ = request.form['inputChamp']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		results = findswb(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = findswbavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/swb">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Suggested Supports for that Bottom Laner</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@application.route('/jwm')
def junglewithmiddle():
	return render_template('jungwmid.html')
	
@application.route('/jwmr',methods=['POST'])
def junglewithmiddleresults():
	_name = request.form['inputName']
	_champ = request.form['inputChamp']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		results = findjwm(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = findjwmavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/jwm">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Suggested Junglers for that Middle Laner</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@application.route('/mwj')
def middlewithjungle():
	return render_template('midwjung.html')
	
@application.route('/mwjr',methods=['POST'])
def middlewithjungleresults():
	_name = request.form['inputName']
	_champ = request.form['inputChamp']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		results = findmwj(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = findmwjavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/mwj">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Suggested Middle Laners for that Jungler</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@application.route('/jwt')
def junglewithtop():
	return render_template('jungwtop.html')
	
@application.route('/jwtr',methods=['POST'])
def junglewithtopresults():
	_name = request.form['inputName']
	_champ = request.form['inputChamp']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		results = findjwt(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = findjwtavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/jwt">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Suggested Junglers for that Top Laner</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@application.route('/twj')
def topwithjungle():
	return render_template('topwjung.html')
	
@application.route('/twjr',methods=['POST'])
def topwithjungleresults():
	_name = request.form['inputName']
	_champ = request.form['inputChamp']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		results = findtwj(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = findtwjavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/twj">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Suggested Top Laners for that Jungler</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@application.route('/svbr',methods=['POST'])
def supportvsbottomresults():
	_name = request.form['inputName']
	_champ = request.form['inputChamp']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		results = findsvb(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = findsvbavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/svb">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Suggested Supports Against that Bottom Laner</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@application.route('/bvsr',methods=['POST'])
def bottomvssupportresults():
	_name = request.form['inputName']
	_champ = request.form['inputChamp']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		results = findbvs(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = findbvsavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/bvs">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Suggested Bottom Laners Against that Support</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@application.route('/lookupresults',methods=['POST'])
def lookuprestuls():
	_champ = request.form['inputChamp']
	_position = request.form['inputPos']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		if _position.lower() not in pos:
			if _position.lower() not in posnn:
				raise Exception('invalid position')
			else:
				postemp = posnn[_position.lower()]
		else:
			postemp = _position.lower()
		results = findlook(tempname, postemp)
		mystr = ''
		for (n, w) in results:
			mystr += (str(n) + ': ' + str((1.0-float(w))) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/lookup">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Good Matchups for this Champion</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')
		
@application.route('/apptest',methods=['POST'])
def apptest():
	_name = request.form['inputName']
	_champ = request.form['inputChamp']
	_position = request.form['inputPos']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		if _position.lower() not in pos:
			if _position.lower() not in posnn:
				raise Exception('invalid position')
			else:
				postemp = posnn[_position.lower()]
		else:
			postemp = _position.lower()
		mystr = ''
		results = suggestion(tempname, _name, postemp)
		
		if len(results) == 0:
			results = findbestavailable(postemp, NAME2ID[tempname])
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/showBasic">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Counter Pick Suggestions</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
		#return redirect("
		#print str(results)
		#return redirect('/')
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')
		#print "error"
		#return redirect('/')

@application.route('/basicblind')
def basicblindsuggestion():
	return render_template('basicblind.html')
	
@application.route('/basicblindresults',methods=['POST'])
def basicblindsuggestionresults():
	_name = request.form['inputName']
	_position = request.form['inputPos']
	try:
		if _position.lower() not in pos:
			if _position.lower() not in posnn:
				raise Exception('invalid position')
			else:
				postemp = posnn[_position.lower()]
		else:
			postemp = _position.lower()
		results = findbasicblind(_name, postemp)
		mystr = ''
		if len(results) == 0:
			results = findbasicblindavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/basicblind">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Blind Pick Suggestions</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@application.route('/c2b')
def counterstoban():
	return render_template('counters2ban.html')

@application.route('/c2br',methods=['POST'])
def counterstobanresults():
	_champ = request.form['inputChamp']
	_position = request.form['inputPos']
	try:
		if _champ not in NAME2ID:
			if _champ in ID2NAME:
				tempname = ID2NAME[_champ]
			elif _champ.lower() in NICKNAMES2NAMES:
				tempname = NICKNAMES2NAMES[_champ.lower()]
			else:
				raise Exception('invalid champion name')
		else:
			tempname = _champ
		champid = NAME2ID[tempname]
		if _position.lower() not in pos:
			if _position.lower() not in posnn:
				raise Exception('invalid position')
			else:
				postemp = posnn[_position.lower()]
		else:
			postemp = _position.lower()
		mystr = ''
		results = findbestavailable(postemp, champid)
		for k in results:
			mystr += (str(k[0])+ ': ' + str(k[1]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/c2b">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Counter Pick to Ban</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@app.route('//riot.txt')
def riotverification():
	return current_app.send_static_file('riot.txt')
	

if __name__ == "__main__":
	application.run()
