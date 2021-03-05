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

### Create config
Create `/etc/config.json` file:
```
{
  "SECRET_KEY": "",
  "EMAIL_USER": "",
  "EMAIL_PASS": "",
	"ALLOWED_HOSTS": "*",
	"DEBUG" : true,
	"WS_PORT": 6379
}
```
EMAIL_USER, EMAIL_PASS are used for password reset with gmail smtp.

### Frontend

`npm install sass`

`sass --watch todochat/app/static/scss:css`

### Collect static for django-ckeditor
`python3 manage.py collectstatic`

### Install ckeditor plugins
* balloonpanel
* balloontoolbar
* cloudservices
* button
* imagebase
* dialog
* easyimage

Plugins needs to be located in `todochat/static/ckeditor/ckeditor/plugins/`


### Migrate and start server

`python3 manage.py migrate`

`docker run -p 6379:6379 -d redis:5`

`python3 manage.py runserver`

## Troubleshooting
### Error: EACCES: permission denied, access '/usr/local/lib' (npm install sass error)**

`sudo npm install sass`

### Problems installing mysqclient

`sudo apt-get install python3-dev default-libmysqlclient-dev build-essential`

## Technologies used
* Django
* WebSockets (django-channels + redis)
* MySQL
* Redis
* HTML / Css / JS
* Bootstrap
* Daphne (for WebSockets) on deployment
* Apache2
