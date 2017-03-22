from flask import Flask, render_template, g, request, redirect, session
from flaskext.mysql import MySQL
import time

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


# (user number, message, delay)
messages = [(0, 'message1', 10),
            (0, '',         5),
            (1, 'message2', 5),
            (1, '',         5),
            (0, 'message3', 2),
            (0, '',         1)]

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

@app.route('/experiment', methods=['GET', 'POST'])
def experiment():
    if request.form:
        cursor.execute("UPDATE `users` SET `message`=%s WHERE `username`=%s",
            [request.form['message'], request.form['user']])
        db.commit()
        return redirect('/experiment')
    else:
        session['num'] += 1
        if session['num'] >= len(messages):
            session['num'] = -1
            return redirect('/admin')

        cursor.execute("SELECT `username` FROM `users` WHERE `type`='user'")
        raw_usernames = cursor.fetchall()
        usernames = []
        for raw_username in raw_usernames:
            usernames.append(raw_username[0])

        return render_template('experiment.html', user=usernames[messages[session['num']][0]],
            message=messages[session['num']][1], delay=messages[session['num']][2])

def sendMessage(username, message, duration, delay):
    print(username, message)
    start = time.time()
    while time.time() - start < delay:
        pass
    cursor.execute("UPDATE `users` SET `message`=%s WHERE `username`=%s", [message, username])
    db.commit()
    start = time.time()
    while time.time() - start < duration:
        pass
    #cursor.execute("UPDATE `users` SET `message`=%s WHERE `username`=%s", ["", username])
    #db.commit()

if __name__ == "__main__":
    app.run()