# CloudyWeb

Cloudyweb is
- CloudyPanel: administration panel for operator
- CloudyService: web service for client

## Prerequisites ##

- python >= 3.4
- pip
- virtualenv/wrapper (optional)

## Installation ##
### Creating the environment (optional) ###
Create a virtual python environment for the project.
If you're not using virtualenv or virtualenvwrapper you may skip this step.

#### For virtualenvwrapper ####
```bash
mkvirtualenv -p /usr/bin/python3 cloudyweb
workon cloudyweb
```

#### For virtualenv ####
```bash
virtualenv -p /usr/bin/python3 cloudyweb-env
cd cloudyweb-env
source bin/activate
```

### Fork & Clone the code ###
Obtain the url to your git repository.

```bash
git clone <URL_TO_GIT_RESPOSITORY>
```

### Install requirements ###
```bash
cd cloudyweb
pip install -r requirements.txt
```

### Sync database ###
```bash
python manage.py migrate
```

## Running ##
```bash
python manage.py runserver
```

Open browser to http://127.0.0.1:8000


## API Usage

    # Create User
    $ curl -X POST http://127.0.0.1:8000/users/ --data "username=john&password=doe"
    ==> {"username":"john","email":"","first_name":"","last_name":""}

    # Retrieving Token
    $ curl -X POST http://127.0.0.1:8000/api-token-auth/ --data "username=john&password=doe"
    ==> {"token":"7f1334b4b27202afe8ef3e078dfc849291e908b9"}

    # Retrieving Resources
    $ curl -X GET http://127.0.0.1:8000/users/ -H 'Authorization: Token abcdefghijklmnopqrstuvwxyz123456790'
	==> [{"username":"john","email":"","first_name":"","last_name":""}, ...]

## List of Resources

* `/users/`
