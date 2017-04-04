from flask import Flask, render_template, g, request, redirect, session
from flaskext.mysql import MySQL
import time
from os import listdir

app = Flask(__name__)

# Secret key is necessary for creating user sessions within the app
app.secret_key = 'D8K27qBS8{8*sYVU>3DA530!0469x{'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'sql9163335'
app.config['MYSQL_DATABASE_PASSWORD'] = 'R3nkreR8cf'
app.config['MYSQL_DATABASE_DB'] = 'sql9163335'
app.config['MYSQL_DATABASE_HOST'] = 'sql9.freemysqlhosting.net'
mysql.init_app(app)

db = mysql.connect()
cursor = db.cursor()

latinSquare = {
    'Order 1' :  [1, 2, 10, 3, 9, 4, 8, 5, 7, 6],
    'Order 2' :  [2, 3, 1, 4, 10, 5, 9, 6, 8, 7],
    'Order 3' :  [3, 4, 2, 5, 1, 6, 10, 7, 9, 8],
    'Order 4' :  [4, 5, 3, 6, 2, 7, 1, 8, 10, 9],
    'Order 5' :  [5, 6, 4, 7, 3, 8, 2, 9, 1, 10],
    'Order 6' :  [6, 7, 5, 8, 4, 9, 3, 10, 2, 1],
    'Order 7' :  [7, 8, 6, 9, 5, 10, 4, 1, 3, 2],
    'Order 8' :  [8, 9, 7, 10, 6, 1, 5, 2, 4, 3],
    'Order 9' :  [9, 10, 8, 1, 7, 2, 6, 3, 5, 4],
    'Order 10' : [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
}

# message format: (user number, message, duration, delay)
messages = [
     # Clip 1
    (0, "Hi there!", 5),
    (0, "", 5),
    (0, "", 20),

    # Clip 2
    (1, "Thank you very much for participating in this experiment.", 3),
    (1, "", 5),
    (1, "", 22),

    # Clip 3
    (2, "Make sure you read all messages displayed even if they are very long.", 14),
    (2, "", 8),
    (2, "", 8),

    # Clip 4
    (3, "You can stop looking at the tablet after you finish reading, even if a message is still there.", 9),
    (3, "", 8),
    (3, "", 13),

    # Clip 5
    (3, "", 30),

    # Clip 6
    (4, "Speaking of really long messages, this is going to be a really long message. It will probably take around 5 seconds to read. Remember to continue the conversation even while reading messages.", 12),
    (4, "", 10),
    (4, "", 8),

    # Clip 7
    (5, "Random facts incoming!", 1),
    (5, "", 5),
    (5, "", 24),

    # Clip 8
    (5, "", 30),

    # Clip 9
    (6, "It's illegal to climb trees in Oshawa, a town in Ontario, Canada.", 22),
    (6, "", 8),

    # Clip 10
    (7, "2 percent of Earth's population naturally has green eyes.", 18),
    (7, "", 8),
    (7, "", 4),

    # Clip 11
    (8, "When you blush, the lining of your stomach also turns red.", 12),
    (8, "", 8),
    (8, "", 10),

    # Clip 12
    (9, "A bolt of lightning is six times hotter than the sun.", 2),
    (9, "", 8),
    (9, "", 20)
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
    return render_template('admin.html')

@app.route('/startExperiment', methods=['GET', 'POST'])
def startExperiment():
    session['order'] = request.form['order']
    files = listdir("Experiments")
    nextNum = int(files[-1][10:-4]) + 1
    file = open("Experiments/Experiment" + ("0" if nextNum < 10 else "") +  str(nextNum) + ".txt", "wb")
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
        file = open("Experiments/Experiment" + session['nextNum'] + ".txt", "a")
        session['num'] += 1
        if session['num'] == 0:
            session['startTime'] = time.time()
        if session['num'] >= len(messages):
            session['num'] = -1
            file.close()
            return redirect('/admin')

        if session['num'] > 0 and messages[session['num'] - 1][1]:
            diff = time.time() - session['startTime']
            #print(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") '" + messages[session['num'] - 1][1] + "' appeared.")
            file.write(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") '" + messages[session['num'] - 1][1] + "' appeared.\n")
        if session['num'] > 0 and messages[session['num'] - 2][1]:
            diff = time.time() - session['startTime']
            #print(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") '" + messages[session['num'] - 2][1] + "' disappeared.")
            file.write(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") '" + messages[session['num'] - 2][1] + "' disappeared.\n")

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