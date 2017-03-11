from flask import Flask, render_template, g
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'sql9163335'
app.config['MYSQL_DATABASE_PASSWORD'] = 'R3nkreR8cf'
app.config['MYSQL_DATABASE_DB'] = 'sql9163335'
app.config['MYSQL_DATABASE_HOST'] = 'sql9.freemysqlhosting.net'
mysql.init_app(app)

cursor = mysql.connect().cursor()

@app.route("/")
def hello():
    cursor.execute("SELECT `message` FROM `users`")
    return render_template("login.html", input=cursor.fetchone()[0])

if __name__ == "__main__":
    app.run()