from flask import Flask, render_template, g, request, redirect, session
from flaskext.mysql import MySQL
import time
from os import listdir

app = Flask(__name__)

# Secret key is necessary for creating user sessions within the app
app.secret_key = 'D8K27qBS8{8*sYVU>3DA530!0469x{'

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'ndass'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MUCproject1'
app.config['MYSQL_DATABASE_DB'] = 'ndass$default'
app.config['MYSQL_DATABASE_HOST'] = 'ndass.mysql.pythonanywhere-services.com'
mysql.init_app(app)

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = mysql.connect()

    return g.mysql_db

def get_cursor():
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = mysql.connect()

    if not hasattr(g, 'cursor'):
        g.cursor = g.mysql_db.cursor()

    return g.cursor

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()

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
    # (0, "5 seconds.mp4", 10),
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
    # (1, "5 seconds.mp4", 3),
    (1, "", 5),
    (1, "", 22),

    # Clip 6
    (2, "never too rich and never too thin", 17),
    # (2, "5 seconds.mp4", 17),
    (2, "", 5),
    (2, "", 8),

    # Clip 7
    (2, "", 30),

    # Clip 8
    (3, "breathing is difficult", 9),
    # (3, "5 seconds.mp4", 9),
    (3, "", 5),
    (3, "", 16),

    # Clip 9
    (3, "", 30),

    # Clip 10
    (4, "I can see the rings on Saturn", 21),
    # (4, "5 seconds.mp4", 21),
    (4, "", 5),
    (4, "", 4),

    # Clip 11
    (4, "", 30),

    # Clip 12
    (4, "", 30),

    # Clip 13
    (5, "physics and chemistry are hard", 15),
    # (5, "5 seconds.mp4", 15),
    (5, "", 5),
    (5, "", 10),

    # Clip 14
    (5, "", 30),

    # Clip 15
    (6, "my bank account is overdrawn", 22),
    # (6, "5 seconds.mp4", 22),
    (6, "", 5),
    (6, "", 3),

    # Clip 16
    (7, "elections bring out the best", 18),
    # (7, "5 seconds.mp4", 18),
    (7, "", 5),
    (7, "", 7),

    # Clip 17
    (8, "we are having spaghetti", 12),
    # (8, "5 seconds.mp4", 12),
    (8, "", 5),
    (8, "", 13),

    # Clip 18
    (8, "", 30),

    # Clip 19
    (8, "", 30),

    # Clip 20
    (9, "time to go shopping", 2),
    # (9, "5 seconds.mp4", 2),
    (9, "", 5),
    (9, "", 23),

    #Clip 21
    (10, "a problem with the engine", 2),
    # (10, "5 seconds.mp4", 2),
    (10, "", 5),
    (10, "", 23),

    #Clip 22
    (11, "elephants are afraid of mice", 2),
    # (11, "5 seconds.mp4", 2),
    (11, "", 5),
    (11, "", 23),

    #Clip 23
    (11, "", 30),

    #Clip 24
    (11, "", 30)
]

# message format: (user number, message, duration, delay)
newMessages = [
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
    (1, "", 6),
    (1, "", 21),

    # Clip 6
    (2, "never too rich and never too thin", 17),
    (2, "", 7),
    (2, "", 6),

    # Clip 7
    (2, "", 30),

    # Clip 8
    (3, "breathing is difficult", 9),
    (3, "", 8),
    (3, "", 13),

    # Clip 9
    (3, "", 30),

    # Clip 10
    (4, "I can see the rings on Saturn", 20),
    (4, "", 9),
    (4, "", 1),

    # Clip 11
    (4, "", 30),

    # Clip 12
    (4, "", 30),

    # Clip 13
    (5, "physics and chemistry are hard", 15),
    (5, "", 10),
    (5, "", 5),

    # Clip 14
    (5, "", 30),

    # Clip 15
    (6, "my bank account is overdrawn", 3),
    (6, "", 11),
    (6, "", 16),

    # Clip 16
    (7, "elections bring out the best", 15),
    (7, "", 12),
    (7, "", 3),

    # Clip 17
    (8, "we are having spaghetti", 12),
    (8, "", 13),
    (8, "", 5),

    # Clip 18
    (8, "", 30),

    # Clip 19
    (8, "", 30),

    # Clip 20
    (9, "time to go shopping", 10),
    (9, "", 14),
    (9, "", 6),

    #Clip 21
    (10, "a problem with the engine", 2),
    (10, "", 15),
    (10, "", 13),

    #Clip 22
    (11, "elephants are afraid of mice", 5),
    (11, "", 16),
    (11, "", 9),

    #Clip 23
    (11, "", 30),

    #Clip 24
    (11, "", 30)
]

messageTexts = [x[1] if x[1] else "No message" for x in messages if x[1] or x[2] == 30]
newMessageTexts = [x[1] if x[1] else "No message" for x in newMessages if x[1] or x[2] == 30]

@app.route("/")
def login():
    session['username'] = ''
    session['num'] = -1
    return render_template("login.html")

@app.route('/processLogin', methods=['GET', 'POST'])
def processLogin():
    username = request.form['username'].lower()
    get_cursor().execute("SELECT `type`, `message` FROM `users` WHERE `username`=%s", [username])
    user_data = get_cursor().fetchone()
    if user_data[0] == 'admin':
        return redirect('/admin')
    else:
        session['username'] = username
        return redirect('/viewer')

@app.route('/viewer')
def viewer():
    get_cursor().execute("SELECT `message` FROM `users` WHERE `username`=%s", [session.get('username')])
    message = get_cursor().fetchone()
    if ".mp4" in message:
        return render_template('video_viewer.html', message=message[0])
    else:
        return render_template('viewer.html', message=message[0])

@app.route('/admin')
def admin():
    session['num'] = -1
    session['clip'] = 1
    return render_template('admin.html')

@app.route('/processAdmin', methods=['GET', 'POST'])
def processAdmin():
    if 'Results' in request.form:
        return redirect('/results')
    elif 'Survey' in request.form:
        return redirect('/survey')
    else:
        # return redirect('/startExperiment')
        return redirect('/startNewExperiment')

@app.route('/survey')
def survey():
    get_cursor().execute("SELECT `experiment` FROM `experiments_40deg`")
    experiments = get_cursor().fetchall()
    return render_template('survey.html', messageTexts=messageTexts, experiments=experiments)

@app.route('/processSurvey', methods=['GET', 'POST'])
def processSurvey():
    get_cursor().execute("""INSERT INTO `surveys_40deg`(`experiment`,`1`,`2`,`3`,`4`,`5`,`6`,`7`,`8`,`9`,
        `10`,`11`,`12`,`13`,`14`,`15`,`16`,`17`,`18`,`19`,`20`,`21`,`22`,`23`,`24`) VALUES (%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        [request.form['experiment'],request.form['1'],request.form['2'],request.form['3'],request.form['4'],
        request.form['5'],request.form['6'],request.form['7'],request.form['8'],request.form['9'],
        request.form['10'],request.form['11'],request.form['12'],request.form['13'],request.form['14'],
        request.form['15'],request.form['16'],request.form['17'],request.form['18'],request.form['19'],
        request.form['20'],request.form['21'],request.form['22'],request.form['23'],request.form['24']])
    get_db().commit()
    return redirect('admin')

@app.route('/results')
def results():
    results = { 'No message (raw)' : {}, '20 degrees' : {}, '30 degrees' : {}, '40 degrees' : {} }
    get_cursor().execute("SELECT * FROM `surveys_5s`")
    rawData = get_cursor().fetchall()
    for rawResults in rawData:
        experiment = rawResults[0]
        get_cursor().execute("SELECT `order` FROM `experiments_5s` WHERE `experiment`=%s", [experiment])
        order = get_cursor().fetchone()[0]
        num = 0

        get_cursor().execute("SELECT `username` FROM `users` WHERE `type`='user'")
        raw_usernames = get_cursor().fetchall()
        usernames = []
        for raw_username in raw_usernames:
            usernames.append(raw_username[0])

        for i, messageText in enumerate(messageTexts):
            rating = str(rawResults[i + 1])
            if messageText == 'No message':
                if rating not in results['No message (raw)']:
                    results['No message (raw)'][rating] = 0
                results['No message (raw)'][rating] += 1
            else:
                # tablet = (latinSquare['Order ' + str(order)][num] - 1) % len(usernames)
                tablet = 2
                num += 1
                if tablet == 0:
                    if rating not in results['20 degrees']:
                        results['20 degrees'][rating] = 0
                    results['20 degrees'][rating] += 1
                elif tablet == 1:
                    if rating not in results['30 degrees']:
                        results['30 degrees'][rating] = 0
                    results['30 degrees'][rating] += 1
                elif tablet == 2:
                    if rating not in results['40 degrees']:
                        results['40 degrees'][rating] = 0
                    results['40 degrees'][rating] += 1
    results['No message'] = {}
    for key in results['No message (raw)']:
        results['No message'][key] = results['No message (raw)'][key] / 3.0
    for key in results:
        get_cursor().execute("""UPDATE `results` SET `Strongly disagree`=%s,`Disagree`=%s,`Slightly disagree`=%s,
            `Neutral`=%s,`Slightly agree`=%s,`Agree`=%s,`Strongly agree`=%s WHERE `Message type`=%s""",
            [results[key]['1'] if '1' in results[key] else '0',
            results[key]['2'] if '2' in results[key] else '0',
            results[key]['3'] if '3' in results[key] else '0',
            results[key]['4'] if '4' in results[key] else '0',
            results[key]['5'] if '5' in results[key] else '0',
            results[key]['6'] if '6' in results[key] else '0',
            results[key]['7'] if '7' in results[key] else '0', key])
        get_db().commit()
    return render_template('results.html', results=results, resultKeys=sorted(results.keys()))

@app.route('/startExperiment')
def startExperiment():
    get_cursor().execute("SELECT `experiment`, `order` FROM `experiments_5s`")
    data = [[x[0] + 1, x[1] + 1] for x in get_cursor().fetchall()]
    next = max(data)
    next[1] = 12 if next[1] % 12 == 0 else next[1] % 12
    orders = range(1,13)
    return render_template('startExperiment.html', next=next, orders=orders)

@app.route('/startNewExperiment')
def startNewExperiment():
    get_cursor().execute("SELECT `experiment`, `order` FROM `experiments_40deg`")
    data = [x[0] + 1 for x in get_cursor().fetchall()]
    next = max(data) if data else 1
    return render_template('startNewExperiment.html', next=next)

@app.route('/processExperiment', methods=['GET', 'POST'])
def processExperiment():
    session['order'] = request.form['order']
    nextNum = int(request.form['nextNum'])
    file = open("/home/ndass/MUC/Experiments/Experiment" + ("0" if nextNum < 10 else "") +  str(nextNum) + ".txt", "wb")
    session['nextNum'] = ("0" if nextNum < 10 else "") +  str(nextNum)
    file.close()
    return redirect('experiment')

@app.route('/processNewExperiment', methods=['GET', 'POST'])
def processNewExperiment():
    nextNum = int(request.form['nextNum'])
    file = open("/home/ndass/MUC/Experiments/Experiment" + ("0" if nextNum < 10 else "") +  str(nextNum) + "_40deg.txt", "wb")
    session['nextNum'] = ("0" if nextNum < 10 else "") +  str(nextNum)
    file.close()
    return redirect('newExperiment')

@app.route('/newExperiment', methods=['GET', 'POST'])
def newExperiment():
    if request.form:
        get_cursor().execute("UPDATE `users` SET `message`=%s WHERE `username`=%s",
            [request.form['message'], request.form['user']])
        get_db().commit()
        return redirect('newExperiment')
    else:
        file = open("/home/ndass/MUC/Experiments/Experiment" + session['nextNum'] + "_40deg.txt", "a")
        session['num'] += 1
        if session['num'] == 0:
            session['startTime'] = time.time()
        if session['num'] >= len(newMessages):
            diff = time.time() - session['startTime']
            file.write(str(int(diff)) + " (" + str(int(diff / 60)) + ":" + str(int(diff - int(diff / 60) * 60)) + ") - Experiment ended.")
            session['num'] = -1
            session['clip'] = 1
            file.close()

            get_cursor().execute("INSERT INTO `experiments_40deg`(`experiment`,`order`) VALUES (%s,%s)",
                [session['nextNum'], -1])
            get_db().commit()

            return redirect('/postNewExperiment')

        if newMessages[session['num']][1] or newMessages[session['num']][2] == 30:
            diff = time.time() - session['startTime']
            file.write(str(int(diff)) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - Clip " + str(session['clip']) + "\n")
            session['clip'] = session['clip'] + 1

        file.close()

        get_cursor().execute("SELECT `username` FROM `users` WHERE `type`='user'")
        raw_usernames = get_cursor().fetchall()
        usernames = []
        for raw_username in raw_usernames:
            usernames.append(raw_username[0])

        return render_template('newExperiment.html', user = usernames[2],
            message = newMessages[session['num']][1], delay = newMessages[session['num']][2], num = session['clip'],
            messageTexts = newMessageTexts)

@app.route('/experiment', methods=['GET', 'POST'])
def experiment():
    if request.form:
        get_cursor().execute("UPDATE `users` SET `message`=%s WHERE `username`=%s",
            [request.form['message'], request.form['user']])
        get_db().commit()
        return redirect('/experiment')
    else:
        file = open("/home/ndass/MUC/Experiments/Experiment" + session['nextNum'] + ".txt", "a")
        session['num'] += 1
        if session['num'] == 0:
            session['startTime'] = time.time()
        if session['num'] >= len(messages):
            diff = time.time() - session['startTime']
            #print(str(diff) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - Experiment ended.")
            file.write(str(int(diff)) + " (" + str(int(diff / 60)) + ":" + str(int(diff - int(diff / 60) * 60)) + ") - Experiment ended.")
            session['num'] = -1
            session['clip'] = 1
            file.close()

            get_cursor().execute("INSERT INTO `experiments_5s`(`experiment`,`order`) VALUES (%s,%s)",
                [session['nextNum'], session['order'].split(' ')[1]])
            get_db().commit()

            return redirect('/postExperiment')

        if messages[session['num']][1] or messages[session['num']][2] == 30:
            diff = time.time() - session['startTime']
            file.write(str(int(diff)) + " (" + str(int(diff / 60)) + ":" + str(diff - int(diff / 60) * 60) + ") - Clip " + str(session['clip']) + "\n")
            session['clip'] = session['clip'] + 1

        file.close()

        get_cursor().execute("SELECT `username` FROM `users` WHERE `type`='user'")
        raw_usernames = get_cursor().fetchall()
        usernames = []
        for raw_username in raw_usernames:
            usernames.append(raw_username[0])

        return render_template('experiment.html', user = usernames[(latinSquare[session['order']][messages[session['num']][0]] - 1) % len(usernames)],
            message = messages[session['num']][1], delay = messages[session['num']][2], order = session['order'], num = session['clip'],
            messageTexts = messageTexts)

@app.route('/postExperiment')
def postExperiment():
    return render_template('postExperiment.html', path="https://www.pythonanywhere.com/user/ndass/files/home/ndass/MUC/Experiments/Experiment" + session['nextNum'] + ".txt")

@app.route('/postNewExperiment')
def postNewExperiment():
    return render_template('postExperiment.html', path="https://www.pythonanywhere.com/user/ndass/files/home/ndass/MUC/Experiments/Experiment" + session['nextNum'] + "_40deg.txt")

if __name__ == "__main__":
    app.run()