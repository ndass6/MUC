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


# message format: (user number, message, delay)
messages = [
             # Clip 1
            (0, "Hi there!", 5),
            (0, "", 5),
            (0, "", 20),

            # Clip 2
            (0, "Thank you very much for participating in this experiment.", 3),
            (0, "", 5),
            (0, "", 22),

            # Clip 3
            (1, "Make sure you read all messages displayed even if they are very long.", 14),
            (1, "", 8),
            (1, "", 8),

            # Clip 4
            (2, "You can stop looking at the tablet after you finish reading, even if a message is still there.", 9),
            (2, "", 8),
            (2, "", 13),

            # Clip 5
            (0, "", 30),

            # Clip 6
            (1, "Speaking of really long messages, this is going to be a really long message. It will probably take around 5 seconds to read. Remember to continue the conversation even while reading messages.", 12),
            (1, "", 10),
            (1, "", 8),

            # Clip 7
            (2, "Random facts incoming!", 1),
            (2, "", 5),
            (2, "", 24),

            # Clip 8
            (0, "", 30),

            # Clip 9
            (0, "It's illegal to climb trees in Oshawa, a town in Ontario, Canada.", 22),
            (0, "", 8),

            # Clip 10
            (0, "2 percent of Earth's population naturally has green eyes.", 18),
            (0, "", 8),
            (0, "", 4),

            # Clip 11
            (2, "When you blush, the lining of your stomach also turns red.", 12),
            (2, "", 8),
            (2, "", 10),

            # Clip 12
            (1, "A bolt of lightning is six times hotter than the sun.", 2),
            (1, "", 8),
            (1, "", 20),

            # Clip 13
            (0, "All pandas in the world are on loan from China.", 15),
            (0, "", 8),
            (0, "", 7),

            # Clip 14
            (1, "After working out, it takes 5 hours for your body temperature to return to normal.", 20),
            (1, "", 8),
            (1, "", 2),

            # Clip 15
            (2, "Halfway done!", 6),
            (2, "", 5),
            (2, "", 19),

            # Clip 16
            (1, "The eye makes movements 50 times every second.", 12),
            (1, "", 8),
            (1, "", 10),

            # Clip 17
            (1, "Sitting straight up is bad for your back. You should slough at an angle of 135 degrees.", 17),
            (1, "", 8),
            (1, "", 5),

            # Clip 18
            (0, "Fruit facts! Strawberries contain more vitamin C than oranges. Banana milkshake is the perfect cure for hangover. Not all oranges are orange. A strawberry is not an actual berry, but a banana is.", 7),
            (0, "", 10),
            (0, "", 13),

            # Clip 19
            (2, "Taking a quick nap after learning can help strengthen your memory.", 7),
            (2, "", 8),
            (2, "", 15),

            # Clip 20
            (0, "", 30),

            # Clip 21
            (2, "Vegetable facts! California produces almost all of the broccoli sold in the United States. Yams and sweet potatoes are not the same thing! A horn worm can eat an entire tomato plant by itself in one day!", 18),
            (2, "", 10),
            (2, "", 2),

            # Clip 22
            (1, "Potato facts! Potatoes first appeared in Europe in 1586. The potato disease 'Late Blight' was the principal cause of the Irish Potato Famine, which killed a half million people.", 14),
            (1, "", 10),
            (1, "", 6),

            # Clip 23
            (1, "Almost done!", 9),
            (1, "", 5),
            (1, "", 16),

            # Clip 24
            (1, "Taking a quick nap after learning can help strengthen your memory.", 24),
            (1, "", 5),
            (1, "", 1),

            # Clip 25
            (2, "Animal facts! Horses and cows sleep while standing up. Even when a snake has its eyes closed, it can still see through its eyelids. Sheep have four stomachs, each one helps them digest the food they eat.", 2),
            (2, "", 10),
            (2, "", 18),

            # Clip 26
            (0, "", 30),

            # Clip 27
            (0, "Two minutes.", 25),
            (0, "", 5),

            # Clip 28
            (0, "Space facts! The Sun is over 300,000 times larger than Earth. Venus is the only planet that spins backwards relative to the other planets. The Sun makes a full rotation once every 25-35 days.", 20),
            (0, "", 10),

            # Clip 29
            (0, "", 30),

            # Clip 30
            (1, "20 seconds!", 10),
            (1, "", 5),
            (1, "", 15)
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

        print(usernames[messages[session['num']][0]] + " " + messages[session['num']][1] + " " + str(messages[session['num']][2]))

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