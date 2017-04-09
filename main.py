from flask import Flask, render_template, g, request, redirect, session
from flaskext.mysql import MySQL
import time
from os import listdir

app = Flask(__name__)

# Secret key is necessary for creating user sessions within the app
app.secret_key = 'D8K27qBS8{8*sYVU>3DA530!0469x{'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'ndass'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MUCproject123'
app.config['MYSQL_DATABASE_DB'] = 'ndass$default'
app.config['MYSQL_DATABASE_HOST'] = 'ndass.mysql.pythonanywhere-services.com'
mysql.init_app(app)

db = mysql.connect()
cursor = db.cursor()

latinSquare = {
    'Order 1'  : [1, 2, 12, 3, 11, 4, 10, 5, 9, 6, 8, 7],
    'Order 2'  : [2, 3, 1, 4, 12, 5, 11, 6, 10, 7, 9, 8],
    'Order 3'  : [3, 4, 2, 5, 1, 6, 12, 7, 11, 8, 10, 9],
    'Order 4'  : [4, 5, 3, 6, 2, 7, 1, 8, 12, 9, 11, 10],
    'Order 5'  : [5, 6, 4, 7, 3, 8, 2, 9, 1, 10, 12, 11],
    'Order 6'  : [6, 7, 5, 8, 4, 9, 3, 10, 2, 11, 1, 12],
    'Order 7'  : [7, 8, 6, 9, 5, 10, 4, 11, 3, 12, 2, 1],
    'Order 8'  : [8, 9, 7, 10, 6, 11, 5, 12, 4, 1, 3, 2],
    'Order 9'  : [9, 10, 8, 11, 7, 12, 6, 1, 5, 2, 4, 3],
    'Order 10' : [10, 11, 9, 12, 8, 1, 7, 2, 6, 3, 5, 4],
    'Order 11' : [11, 12, 10, 1, 9, 2, 8, 3, 7, 4, 6, 5],
    'Order 12' : [12, 1, 11, 2, 10, 3, 9, 4, 8, 5, 7, 6]
}

# message format: (user number, message, duration, delay)
messages = [
     # Clip 1
    (0, "my watch fell in the water", 10),
    (0, "", 5),
    (0, "", 15),

    # Clip 2
    (0, "", 30),

    # Clip 3
    (0, "", 30),

    # Clip 4
    (0, "", 30),

    # Clip 5
    (1, "prevailing wind from the east", 3),
    (1, "", 5),
    (1, "", 22),

    # Clip 6
    (2, "never too rich and never too thin", 17),
    (2, "", 5),
    (2, "", 8),

    # Clip 7
    (2, "", 30),

    # Clip 8
    (3, "breathing is difficult", 9),
    (3, "", 5),
    (3, "", 16),

    # Clip 9
    (3, "", 30),

    # Clip 10
    (4, "I can see the rings on Saturn", 21),
    (4, "", 5),
    (4, "", 4),

    # Clip 11
    (4, "", 30),

    # Clip 12
    (4, "", 30),

    # Clip 13
    (5, "physics and chemistry are hard", 15),
    (5, "", 5),
    (5, "", 10),

    # Clip 14
    (5, "", 30),

    # Clip 15
    (6, "my bank account is overdrawn", 22),
    (6, "", 5),
    (6, "", 3),

    # Clip 16
    (7, "elections bring out the best", 18),
    (7, "", 5),
    (7, "", 7),

    # Clip 17
    (8, "we are having spaghetti", 12),
    (8, "", 5),
    (8, "", 13),

    # Clip 18
    (8, "", 30),

    # Clip 19
    (8, "", 30),

    # Clip 20
    (9, "time to go shopping", 2),
    (9, "", 5),
    (9, "", 23),

    #Clip 21
    (10, "a problem with the engine", 2),
    (10, "", 5),
    (10, "", 23),

    #Clip 22
    (11, "elephants are afraid of mice", 2),
    (11, "", 5),
    (11, "", 23),

    #Clip 23=
    (11, "", 30),

    #Clip 24
    (11, "", 30)
]

@app.route("/")
def login():
    session['username'] = ''
    session['num'] = -1
    return render_template("login.html")

@app.route('/processLogin', methods=['GET', 'POST'])
def processLogin():
    username = request.form['username'].lower()
    cursor.execute("SELECT `type`, `message` FROM `users` WHERE `username`=%s", [username])
    user_data = cursor.fetchone()
    if user_data[0] == 'admin':
        return redirect('/admin')
    else:
        session['username'] = username
        return redirect('/viewer')

@app.route('/viewer')
def viewer():
    cursor.execute("SELECT `message` FROM `users` WHERE `username`=%s", [session.get('username')])
    message = cursor.fetchone()
    return render_template('viewer.html', message=message[0])

@app.route('/admin')
def admin():
    session['num'] = -1
    session['clip'] = 1
    return render_template('admin.html')

@app.route('/startExperiment', methods=['GET', 'POST'])
def startExperiment():
    session['order'] = request.form['order']
    files = listdir("/home/ndass/MUC/Experiments")
    nextNum = int(files[-2][10:-4]) + 1
    file = open("/home/ndass/MUC/Experiments/Experiment" + ("0" if nextNum < 10 else "") +  str(nextNum) + ".txt", "wb")
    session['nextNum'] = ("0" if nextNum < 10 else "") +  str(nextNum)
    file.close()
    return redirect('experiment')

@app.route('/experiment', methods=['GET', 'POST'])
def experiment():
    if request.form:
        cursor.execute("UPDATE `users` SET `message`=%s WHERE `username`=%s",
            [request.form['message'], request.form['user']])
        db.commit()
        return redirect('/experiment')
    else:
        file = open("/home/ndass/MUC/Experiments/Experiment" + session['nextNum'] + ".txt", "a")
        session['num'] += 1
        if session['num'] == 0:
            session['startTime'] = time.time()
        if session['num'] >= len(messages):
            diff = time.time() - session['startTime']
            #print(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - Experiment ended.")
            file.write(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - Experiment ended.")
            session['num'] = -1
            session['clip'] = 1
            file.close()
            return redirect('/admin')

        if messages[session['num']][1] or messages[session['num']][2] == 30:
            diff = time.time() - session['startTime']
            #print(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - Clip " + str(session['clip']) + "\n")
            file.write(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - Clip " + str(session['clip']) + "\n")
            session['clip'] = session['clip'] + 1
        if session['num'] > 0 and messages[session['num'] - 1][1]:
            diff = time.time() - session['startTime']
            #print(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - '" + messages[session['num'] - 1][1] + "' appeared.")
            file.write(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - '" + messages[session['num'] - 1][1] + "' appeared.\n")
        if session['num'] > 0 and messages[session['num'] - 2][1]:
            diff = time.time() - session['startTime']
            #print(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") '" + messages[session['num'] - 2][1] + "' disappeared.")
            file.write(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - '" + messages[session['num'] - 2][1] + "' disappeared.\n")

        file.close()

        cursor.execute("SELECT `username` FROM `users` WHERE `type`='user'")
        raw_usernames = cursor.fetchall()
        usernames = []
        for raw_username in raw_usernames:
            usernames.append(raw_username[0])

        return render_template('experiment.html', user=usernames[(latinSquare[session['order']][messages[session['num']][0]] - 1) % len(usernames)],
            message=messages[session['num']][1], delay=messages[session['num']][2], order=session['order'])

if __name__ == "__main__":
    app.run()