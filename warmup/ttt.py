from flask import Flask,request, render_template, jsonify
import datetime, random
app = Flask(__name__)



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
	board = request.get_json()['grid']
	empty = []
	a = b = 0
	for x in range(len(board)):
		if board[x] =='X':
			a+=1
		elif board[x] =='O':
			b+=1
		else:
			empty.append(x)
	if a>b:
		me = 'O'
		you = 'X'
	else:
		me = 'X'
		you = 'O'
	#player win
	if check(board,you):
		return jsonify(grid = board, winner = you)
	#server move or declare null
	if len(empty) != 0:
		ran = random.randint(0, len(empty)-1)
		board[empty[ran]] = me
	else:
		return jsonify(grid = board, winner = ' ')
	#server win
	if check(board,me):
		return jsonify(grid = board, winner = me)
	#pass back to player
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

if __name__ == "__main__":
#	app.debug = True
	app.run(host='0.0.0.0',port=80)

