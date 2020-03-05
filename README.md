# Action2Phone
*"A service only a fellow comrade could love"* -FSB

This is the technical assesment for Phone2Action. Please note the work product of this assignment is a parody and no malice is intended. Hopefully you have a sense of humor.

### Submission page
![screenshot1](https://github.com/paulpierre/p2a_assessment/blob/master/art/screenshot1.png?raw=true)

### SMS page
![screenshot2](https://github.com/paulpierre/p2a_assessment/blob/master/art/screenshot2.png?raw=true)

### How to run it

Ensure you have Python3 installed on your system. Virtual environment and packages should already be installed, just load the virtual env:

`source env/bin/active`

If you need to re-install packages:

`pip install -r requirements.txt`

## Architecture
Given the limited amount of time the following was used:
* Python3
* Flask REST micro-framework
* Jinja templating
* Bootstrap 4
* SQLite3
* jQuery

Normally I user VueJS but jQuery on a CDN does the job quicker.
Additionally I would have preferred to deploy this in a container.

### Additional time

Given additional time, obvious stand out things to address:
* Sanitizing user input properly
* User registration rather than hardcoding auth
* Containerization for scalability
* MySQL or Postgres for scalability and redundancy
* Separate login / registration screens or pop-overs
* Leverage Flask plugins for forms
* Leverage PeeWee ORM (I've included it but did not use it due to time)
* User sessions / JWT tokens
* Security in APIs
* Deeper integration w/ Twilio and error handling
* Leverage cloud infra (Kubernetes)
* Place credentials and settings in ENV VARS
* Writing some unit tests in pytest and maybe pyppeteer for JS
* Funnier text

## Database
I went with sqlite3 for storage since it is convenient due to the local nature of the storage and it comes bundled with the latest versions of OSX and most Linux environments


### Browse database
If you want to browser the database you can just run sqlite3 in Terminal and type the following:
```
sqlite3
.open db/p2a_db.sqlite
.schema users
```

### Testing Twilio
If you'd like to test the Twilio SDK functionality, please switch out your own tokens here:
```python
TWILIO_SID = '#####################'
TWILIO_TOKEN = '#####################'
```

Additionally if you'd like the app to actually send to your own phone number to see that it works do the following:

```
sqlite3
.open db/p2a_db.sqlite
UPDATE users SET user_phone_number = '+17031234568';
SELECT * FROM users
```