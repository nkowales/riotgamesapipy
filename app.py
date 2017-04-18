from flask import Flask, render_template, json, request, redirect
from id2name import NAME2ID
from id2name import ID2NAME
from nicknames2names import NICKNAMES2NAMES
import dbfuncs

pos = ['supp', 'bot', 'mid', 'jungle', 'top']#valid position entries
posnn = {'support' : 'supp', 'sup' : 'supp', 'adc' : 'bot', 'bottom' : 'bot', 'middle' : 'mid', 'solomid' : 'mid', 'jung' : 'jungle', 'jun' : 'jungle', 'j' : 'jungle'}#common alternate position names

app = Flask(__name__)
@app.route("/")
def main():
	return render_template('index.html')

@app.route('/showBasic')
def showBasic():
	return render_template('basicsuggestion.html')

@app.route('/lookup')
def lookup():
	return render_template('lookup.html')
	
@app.route('/svb')
def supportvsbottom():
	return render_template('suppvbot.html')
	
@app.route('/svbr',methods=['POST'])
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
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/svb">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Results</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')

@app.route('/lookupresults',methods=['POST'])
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
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/lookup">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Results</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')
		
		

@app.route('/apptest',methods=['POST'])
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
		
		return '<head>' + '<title>League of Legends Suggestion</title>' + '<link href="../static/bootstrap.min.css" rel="stylesheet">' + '<link href="../static/jumbotron-narrow.css" rel="stylesheet">' + '</head>' + '<body>' + '<div class="container">' + '<div class="header">' + '<nav>' + '<ul class="nav nav-pills pull-right">' + '<li role="presentation" class="active"><a href="/">Home</a></li>' + '<li role="presentation"><a href="/showBasic">Back</a></li>' + '</ul>' + '</nav>' + '<h3 class="text-muted">League of Legends Suggestion App</h3>' + '</div>' + '<div class="jumbotron">' + '<h1>Results</h1>' + '<h9>' + mystr + '</h9>' + '</div>' + '</div>' + '</body>' 
		#return redirect("
		#print str(results)
		#return redirect('/')
	except Exception as e:
		return json.dumps('<span>'+str(e)+'</span>')
		#print "error"
		#return redirect('/')

if __name__ == "__main__":
	app.run()
