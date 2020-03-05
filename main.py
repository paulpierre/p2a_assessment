import sqlite3
import json
from twilio.rest import Client
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, Response, jsonify

app = Flask(__name__)


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



# Default page
# ------------

@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html')


# Admin authentication end-point
# ------------------------------

@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_login = request.form.get('user_name')
    user_password = request.form.get('user_password')

    print(f'Received data: {json.dumps(request.form)}')
    print(f'user_login: {user_login} user_password: {user_password}')
    m = hashlib.md5()

    m.update(bytes(user_login, encoding='utf-8') + bytes(user_password, encoding='utf-8'))
    user_hash = m.hexdigest()

    print(f'user hash: {user_hash}')

    if user_hash == LOGIN_HASH:
        print('user authenticated!')
        return jsonify({'response': 1, 'url': f'/dashboard/{user_hash}'})
    else:
        print('User NOT authenticated')
        return jsonify({'response': 0})


# Form submission end-point
# -------------------------

@app.route('/submit', methods=['POST'])
def submit():

    user_first_name = request.form.get('user_first_name')
    user_last_name = request.form.get('user_last_name')
    user_email = request.form.get('user_email')
    user_phone = request.form.get('user_phone')



    print(f'Received data: {json.dumps(request.form)}')

    if user_first_name and user_last_name and user_email and user_phone:

        user_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # lets add this to the database
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        c.execute(f'''
            INSERT INTO users (user_first_name, user_last_name, user_email, user_phone_number, user_date) VALUES('{user_first_name}','{user_last_name}','{user_email}','{user_phone}','{user_date}');
        ''')
        conn.commit()
        conn.close()

        return jsonify({'response': 1})
    else:
        return jsonify({'response': 0})


# SMS page
# --------

@app.route('/dashboard/<user_hash>', methods=['GET', 'POST'])
def dashboard(user_hash):

    if user_hash == LOGIN_HASH:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        user_list = list()
        for row in conn.execute("SELECT * FROM users"):
            user_list.append({
                'user_id':row[0],
                'user_first_name':row[1],
                'user_last_name': row[2],
                'user_email': row[3],
                'user_phone': row[4],
                'user_date': row[5]
            })
        conn.close()
        return render_template('dashboard.html', user_list=user_list)
    else:
        return Response(status=403)


# SMS end-point
# -------------

@app.route('/sms', methods=['POST'])
def sms():
    data = request.get_json()

    if not data:
        return jsonify({'response': 0})

    print(f'Received {json.dumps(data,indent=4)}')

    user_list = [i.split('=')[1] for i in data['users'].split('&')]
    message = data['message']
    user_list.append('+17033036520')
    print(f'sending "{message}" to numbers: {json.dumps(user_list,indent=4)}')

    try:
        # Lets authenticate
        client = Client(TWILIO_SID, TWILIO_TOKEN)

        for phone_number in user_list:
            print(f'sending "{message}" to {phone_number}')
            message = client.messages.create(
                to=f"{phone_number}",
                from_="+12055397014",
                body=message)
            print(message.sid)

    except:
        print('There was an error sending SMS')
        return jsonify({'response': 0})

    print('SMS was sent successfully!')
    return jsonify({'response': 1})



# Main
# ----

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=31337, debug=True)
