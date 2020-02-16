[![Build Status](https://travis-ci.com/n3rsti/ToDoChat.svg?branch=master)](https://travis-ci.com/n3rsti/ToDoChat)
# ToDoChat
## Setup
### Setup virtual environment

```
virtualenv -p python3 venv/
source venv/bin/activate
```

### Install packages

`pip3 install -r requirements.txt`

### Setup database
Fill **my.cnf** with MySQL informations

`sudo nano /etc/mysql/my.cnf`

```
[client]
database = db_name
user = user
password = mysql_password
default-character-set = utf8
```
### Frontend

`npm install sass`

`sass --watch todochat/app/static/scss:css`

### Migrate and start server

`python3 manage.py migrate`

`python3 manage.py runserver`

## Troubleshooting
### Error: EACCES: permission denied, access '/usr/local/lib' (npm install sass error)**

`sudo npm install sass`

### Problems installing mysqclient

`sudo apt-get install libssl-dev`
