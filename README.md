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

### Migrate and start server

`python3 manage.py migrate`
`python3 manage.py runserver`
