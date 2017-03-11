from flask import Flask, render_template, g, request, redirect, session
from flaskext.mysql import MySQL

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

@app.route("/")
def login():
    session['username'] = ''
    return render_template("login.html")

@app.route('/processLogin', methods=['GET', 'POST'])
def processLogin():
    username = request.form['username']
    password = request.form['password']
    cursor.execute("SELECT `type`, `message` FROM `users` WHERE `username`=%s AND `password`=%s", [username, password])
    user_data = cursor.fetchone()
    if user_data[0] == 'admin':
        cursor.execute("SELECT `username` FROM `users` WHERE `type`='user'")
        usernames = cursor.fetchone()
        return render_template('admin.html', usernames=usernames)
    else:
        session['username'] = username
        return redirect('/showMessage')

@app.route('/showMessage')
def showMessage():
    print('showing message')
    cursor.execute("SELECT `message` FROM `users` WHERE `username`=%s", [session.get('username')])
    message = cursor.fetchone()
    return render_template('user.html', message=message[0])

@app.route('/sendMessage', methods=['GET', 'POST'])
def sendMessage():
    username = request.form['username']
    message = request.form['message']
    print(username, message)
    cursor.execute("UPDATE `users` SET `message`=%s WHERE `username`=%s", [message, username])
    db.commit()

    cursor.execute("SELECT `username` FROM `users` WHERE `type`='user'")
    usernames = cursor.fetchall()
    return render_template('admin.html', usernames=usernames)


if __name__ == "__main__":
    app.run()