from flask import Flask, request, render_template, jsonify, make_response
from flask_mail import Mail, Message
from bson.objectid import ObjectId
import datetime, random, smtplib
from pymongo import MongoClient

client = MongoClient()
db = client.warmup2
w2u = db.users
w2g = db.games
tttgrid = False

app = Flask(__name__)
mail = Mail(app)

@app.route('/adduser', methods = ['GET','POST'])
def au():
	if request.method == 'GET':
                return render_template('form.html', nu = 'true')
	if request.method == 'POST':
		nuser =  request.get_json()
		userstat= {
			'user' : nuser['username'],
			'password' : nuser['password'],
			'email' : nuser['email'],
			'key' : 'abracadabra',
			'verify' : 'no',
			'win' : 0,
			'lose' : 0,
			'tie' : 0,
			'games' :[],
			'board' : None
		}
		w2u.insert_one(userstat)
		vmailstr = "validation key: <"+"abracadabra"+">"
		msg = Message(recipients = [nuser['email']], body = vmailstr,
			sender = 'ansible-receipt.cloud.compas.cs.stonybrook.edu')
		try:
			mail.send(msg)
			return jsonify(status = 'OK')
		except Exception as ex:
			print(ex)
			return jsonify(status = 'ERROR')

@app.route('/verify', methods = ['GET','POST'])
def ver():
	if request.method == 'POST':
		vreq =  request.get_json()
		mcheck = w2u.find_one({'email' : vreq['email'], 'key' : vreq['key']})
		if (mcheck is None):
			return jsonify(status = 'ERROR')
		else:
			w2u.update_one(mcheck, {"$set" : { 'verify' : 'yes'}})
			return jsonify(status = 'OK')

@app.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		lreq = request.get_json()
		luser =  w2u.find_one({'user' : lreq['username'], 'password' : lreq['password']})
		if luser is None or luser['verify'] != 'yes':
			return jsonify(status = 'ERROR')
		else:
			r = make_response(jsonify(status = 'OK'))
			r.set_cookie('user', lreq['username'])
			return r

@app.route('/logout', methods = ['GET','POST'])
def logout():
	u = request.cookies.get('user')
	if u is None:
		return jsonify(status = 'ERROR')
	else:
		resp = make_response()
		resp.set_cookie('user','',expires=0)
		return jsonify(status = 'OK')

@app.route('/ttt', methods = ['GET','POST'])
def name():
	a = datetime.datetime(1,2,3)
	a= a.today()
	if request.method == 'GET':
		return render_template('index.html')
	if request.method == 'POST':
		return render_template('index.html', name=request.form['name'], date =a)

@app.route('/ttt/play', methods = ['POST'])
def ttt():
	u = request.cookies.get('user')
	if u is None:
		return jsonify(status = 'ERROR')
	udata = w2u.find_one({'user' : u })
	if udata['board'] is None:
		board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
		gboard = {
			'user' : u,
			'board': board,
			'win' : ' ',
		}
		tid = w2g.insert_one(gboard)
		a = datetime.datetime(1,2,3)
		a= a.today()
		gstat = udata['games']
		gstat.append({'id':str(tid.inserted_id), 'start_date':a})
		w2u.update_one({'user' : u }, {"$set": {'games' : gstat}})
	else:
		board = udata['board']
	print(board, udata['games'][-1])
	gid = udata['games'][-1]['id']
	w2u.update_one({'user' : u }, {"$set": {'board' : board}})
	move = request.get_json()['move']
	if move is None:
		return jsonify(grid = board, winner = ' ')
	board[move] = 'X' #player is X
	print(board,move)
	w2u.update_one({'user' : u }, {"$set": {'board' : board}})
	w2g.update_one({'_id' : ObjectId(gid) }, {"$set": {'board': board}})
	empty = []
	for x in range(len(board)):
		if board[x] !='X' and board[x] != 0:
			empty.append(x)
	#player win
	if check(board,'X'):
		w2g.update_one({'_id' : ObjectId(gid)}, {"$set": {'win': 'X', 'board': board}})
		w2u.update_one({'user' : u }, {"$set": {'win' : udata['win']+1, 'board' : None}})
		return jsonify(grid = board, winner = 'X')
	#server move or declare null
	if len(empty) != 0:
		ran = random.randint(0, len(empty)-1)
		board[empty[ran]] = 'O'
		w2u.update_one({'user' : u }, {"$set": {'board' : board}})
		w2g.update_one({'_id' : ObjectId(gid) }, {"$set": {'board': board}})
		print(board,'end')
	else:
		w2g.update_one({'_id' : ObjectId(gid) }, {"$set": {'win': ' ', 'board': board}})
		w2u.update_one({'user' : u }, {"$set": {'tie' : udata['tie']+1, 'board' : None}})
		return jsonify(grid = board, winner = ' ')
	#server win
	if check(board,'O'):
		w2g.update_one({'_id' : ObjectId(gid)}, {"$set": {'win': 'O'}, 'board' : board})
		w2u.update_one({'user' : u }, {"$set": {'lose' : udata['lose']+1, 'board' : None}})
		return jsonify(grid = board, winner = 'O')
	#pass back to player
	w2u.update_one({'user' : u }, {"$set": {'board' : board}})
	w2g.update_one({'_id' : ObjectId(gid) }, {"$set": {'board': board}})
	return jsonify(grid = board, winner = ' ')
def check(grid,side):
	ans = False
	if grid[0] == side:
		ans = check3(side,grid[3],grid[6]) or check3(side,grid[1],grid[2]) or check3(side,grid[4],grid[8]) or ans
	if grid[1] == side:
		ans = check3(side,grid[4],grid[7]) or ans
	if grid[2] == side:
		ans = check3(side,grid[5],grid[8]) or check3(side,grid[4],grid[6]) or ans
	if grid[3] == side:
		ans = check3(side,grid[4],grid[5]) or ans
	if grid[6] == side:
		ans = check3(side,grid[7],grid[8]) or ans
	return ans
def check3(a,b,c):
	return a==b and b==c 

@app.route('/listgames', methods = ['POST'])
def lg():
	u = request.cookies.get('user')
	if u is None:
		return jsonify(status = 'ERROR')
	udata = w2u.find_one({'user' : u })
	g = udata['games']
	return jsonify(status='OK', games=g)

@app.route('/getgame', methods = ['POST'])
def gg():
	g = request.get_json()['id']
	if g is None:
		return jsonify(status = 'ERROR')
	gdata = w2g.find_one({'_id': ObjectId(g)})
	print(gdata)
	return jsonify(status='OK', grid = gdata['board'], winner = gdata['win'])

@app.route('/getscore', methods = ['POST'])
def gs():
	u = request.cookies.get('user')
	if u is None:
		return jsonify(status = 'ERROR')
	udata = w2u.find_one({'user' : u })
	return jsonify(status='OK', human=udata['win'], wopr=udata['lose'], tie=udata['tie'])

if __name__ == "__main__":
#	app.debug = True
	app.run(host='0.0.0.0',port=80)

