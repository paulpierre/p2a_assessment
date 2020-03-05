# Action2Phone
"A service only a fellow comrade could love"

This is the technical assesment for Phone2Action. Please note the work product of this assignment is a parody and no malice is intended. Hopefully you have a sense of humor.

### How I set it up
python3 -m venv env


## Architecture
Given the limited amount of time the following was used:
* Python3
* Flask REST micro-framework
* Jinja templating
* Bootstrap 4
* SQLite3
* jQuery

I swear I don't use jQuery normally but for quick prototypes it does the job.
In other circumstances I would use vanilla JS or vue.js. Additionally I would likely deploy this in a container.

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
If you'd like to test the Twilio SDK functionality, please switch out your own tokens

Additionally if you'd like the app to actually send to your own phone number to see that it works do the following:

```
sqlite3
.open db/p2a_db.sqlite
UPDATE users SET user_phone_number = '+17031234568';
SELECT * FROM users
```