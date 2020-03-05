import sqlite3
import json
from twilio.rest import Client
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, Response, jsonify

app = Flask(__name__)

# ===========
# GLOBAL VARS
# ===========

# Credentials
# -----------

ADMIN_LOGIN = 'admin@action2phone.com'
ADMIN_PASSWORD = 'letmeinfancybear'

TWILIO_SID = '#####################'
TWILIO_TOKEN = '#####################'


# MD5 Hash setup
# --------------

m = hashlib.md5()
m.update(bytes(ADMIN_LOGIN, encoding='utf-8') + bytes(ADMIN_PASSWORD, encoding='utf-8'))
LOGIN_HASH = m.hexdigest()

print(f'login hash: {LOGIN_HASH}')

# Path to SQLite3 DB
# ------------------

DB_FILE = 'db/p2a_db.sqlite'


# ======
# ROUTES
# ======

# Default page
# ------------

@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')


# Admin authentication end-point
# ------------------------------

@app.route('/authenticate', methods=['POST'])
def authenticate():

    # Grab username and password from HTTP request
    user_login = request.form.get('user_name')
    user_password = request.form.get('user_password')

    print(f'Received data: {json.dumps(request.form)}')
    print(f'user_login: {user_login} user_password: {user_password}')

    # Lets setup the MD5 hash and make sure we encode the strings
    m = hashlib.md5()
    m.update(bytes(user_login, encoding='utf-8') + bytes(user_password, encoding='utf-8'))
    user_hash = m.hexdigest()

    print(f'user hash: {user_hash}')

    # If the hashes match let them in and give them the unique URL
    if user_hash == LOGIN_HASH:
        print('user authenticated!')
        return jsonify({'response': 1, 'url': f'/dashboard/{user_hash}'})

    # If it does not, they suck
    else:
        print('User NOT authenticated')
        return jsonify({'response': 0})


# Form submission end-point
# -------------------------

@app.route('/submit', methods=['POST'])
def submit():

    # Lets setup the variables from the HTTP rrequest
    user_first_name = request.form.get('user_first_name')
    user_last_name = request.form.get('user_last_name')
    user_email = request.form.get('user_email')
    user_phone = request.form.get('user_phone')

    print(f'Received data: {json.dumps(request.form)}')

    # If they provided the requisite data to insert ..
    if user_first_name and user_last_name and user_email and user_phone:

        # Lets get the current time in the format that we like
        user_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Lets setup the database connection and cursor
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # Normally we'd use an ORM, but we're tight on time
        c.execute(f'''
            INSERT INTO users (user_first_name, user_last_name, user_email, user_phone_number, user_date) VALUES('{user_first_name}','{user_last_name}','{user_email}','{user_phone}','{user_date}');
        ''')

        # Commit the data and close the database connection
        conn.commit()
        conn.close()

        # Respond with success
        return jsonify({'response': 1})

    # Or they suck
    else:
        return jsonify({'response': 0})


# SMS page
# --------

@app.route('/dashboard/<user_hash>', methods=['GET', 'POST'])
def dashboard(user_hash):

    # Lets check again that this is a valid hash based on the credentials above
    if user_hash == LOGIN_HASH:

        # Lets intialize a connection to the DB
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # We create the array
        user_list = list()

        # Next we iterate over the results
        for row in conn.execute("SELECT * FROM users"):

            # And we append it to the array
            user_list.append({
                'user_id':row[0],
                'user_first_name':row[1],
                'user_last_name': row[2],
                'user_email': row[3],
                'user_phone': row[4],
                'user_date': row[5]
            })

        # We close the database and return the list (array) to our template for it to process
        conn.close()

        # Display the template
        return render_template('dashboard.html', user_list=user_list)
    else:

        # They suck
        return Response(status=403)


# SMS end-point
# -------------

@app.route('/sms', methods=['POST'])
def sms():

    # Lets grab the JSON data from the HTTP request
    data = request.get_json()

    # If they've brought nothing to the table.. then they suck
    if not data:
        return jsonify({'response': 0})

    print(f'Received {json.dumps(data,indent=4)}')

    # Lets get fancy and use a tidy yet confusing list comprehension. This breaks apart
    # the query string and puts the phone numbers in an indexed array so we may iterate over it later
    user_list = [i.split('=')[1] for i in data['users'].split('&')]

    # Lets set the message
    message = data['message']

    print(f'sending "{message}" to numbers: {json.dumps(user_list,indent=4)}')

    try:
        # Lets authenticate
        client = Client(TWILIO_SID, TWILIO_TOKEN)

        # Lets go through each phone number and send a message in Twilio
        for phone_number in user_list:
            print(f'sending "{message}" to {phone_number}')
            message = client.messages.create(
                to=f"{phone_number}",
                from_="+12055397014",
                body=message)
            print(message.sid)

    except:
        # Maybe we or they suck, who knows
        print('There was an error sending SMS')
        return jsonify({'response': 0})

    # Hopefully we did something right and you got the SMS. I know I did :)
    print('SMS was sent successfully!')
    return jsonify({'response': 1})



# Main
# ----

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=31337, debug=True)
