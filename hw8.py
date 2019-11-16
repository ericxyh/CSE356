import mysql.connector, csv, pylibmc
from flask import Flask, request, render_template, jsonify, make_response

mc = pylibmc.Client(["127.0.0.1"])

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="62771464",
    database="hw8"
)

cursor = mydb.cursor()
#cursor.execute("CREATE TABLE assists (Player VARCHAR(255),Club VARCHAR(255), POS VARCHAR(255),GP INTEGER, GS INTEGER, A INTEGER,GWA INTEGER, HmA INTEGER, RdA INTEGER, A90min FLOAT) CHARACTER SET utf8 COLLATE utf8_unicode_ci")

'''with open('assists.csv') as csvfile:
    reader = csv.reader(csvfile)
    columns = next(reader)
    query = 'insert into assists ({0}) values ({1})'
    query = query.format(','.join(columns), ','.join(['%s'] * len(columns)))
    print(query)
    for row in reader:
        print(row)
        print(', '.join(row))
        cursor.execute(query, row)
    mydb.commit()
'''
#SELECT Player, A FROM assists WHERE Club='HOU' and POS='D' ORDER BY A DESC, GS DESC,Player

app = Flask(__name__)

@app.route('/hw8', methods = ['GET'])
def getdata():
    club = request.args.get('club')
    pos = request.args.get('pos')
    cp = club+'_'+pos
    if cp in mc:
        return mc[cp]
    else:
        cursor.execute("SELECT Player, A FROM assists WHERE Club=%s and POS=%s ORDER BY A DESC, GS DESC,Player", (club,pos))
        myresult = cursor.fetchall()
        av = 0
        for x in myresult:
            av += x[-1]
        av /= float(len(myresult))
        j = jsonify(club=club,pos=pos, max_assists=myresult[0][-1], player=myresult[0][0], avg_assists = av)
        mc[cp] = j
        return j


if __name__ == "__main__":
#	app.debug = True
	app.run(host='0.0.0.0',port=80)
