from flask import Flask, render_template, json, request, redirect
from id2name import NAME2ID
from id2name import ID2NAME
from nicknames2names import NICKNAMES2NAMES
import dbfuncs

pos = ['supp', 'bot', 'mid', 'jungle', 'top']#valid position entries
posnn = {'support' : 'supp', 'sup' : 'supp', 'adc' : 'bot', 'bottom' : 'bot', 'middle' : 'mid', 'solomid' : 'mid', 'jung' : 'jungle', 'jun' : 'jungle', 'j' : 'jungle'}#common alternate position names

application = Flask(__name__)
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
	results = dbfuncs.findbans()
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
		results = dbfuncs.findbws(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = dbfuncs.findbwsavailable(tempname) 
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
		results = dbfuncs.findswb(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = dbfuncs.findswbavailable(tempname) 
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
		results = dbfuncs.findjwm(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = dbfuncs.findjwmavailable(tempname) 
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
		results = dbfuncs.findmwj(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = dbfuncs.findmwjavailable(tempname) 
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
		results = dbfuncs.findjwt(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = dbfuncs.findjwtavailable(tempname) 
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
		results = dbfuncs.findtwj(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = dbfuncs.findtwjavailable(tempname) 
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
		results = dbfuncs.findsvb(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = dbfuncs.findsvbavailable(tempname) 
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
		results = dbfuncs.findbvs(_name, tempname)
		mystr = ''
		if len(results) == 0:
			results = dbfuncs.findbvsavailable(tempname) 
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
		results = dbfuncs.findlook(tempname, postemp)
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
		results = dbfuncs.suggestion(tempname, _name, postemp)
		
		if len(results) == 0:
			results = dbfuncs.findbestavailable(postemp, NAME2ID[tempname])
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
		results = dbfuncs.findbasicblind(_name, postemp)
		mystr = ''
		if len(results) == 0:
			results = dbfuncs.findbasicblindavailable(tempname) 
			for (n, w) in results:
				mystr += (str(n) + ': ' + str(w) + '<br/>')
		else:
			for k in results:
				mystr += (str(k[0])+ ': ' + str(k[2]) + '<br/>')
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/basicblind">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Blind Pick Suggestions</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')



if __name__ == "__main__":
	application.run()
