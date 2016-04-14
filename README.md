# CloudyWeb

Cloudyweb is
- CloudyPanel: administration panel for operator
- CloudyService: web service for client

Continuous Integration:

[![Build Status](https://travis-ci.org/insert-coin/cloudyweb.svg?branch=master)](https://travis-ci.org/insert-coin/cloudyweb)

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

### Local Settings ###

Copy the `__local_settings.py` template as `local_settings.py`
You are free to overwrite any existing `settings.py` 
for your local development.

```bash
cp cloudyweb/{__,}local_settings.py
```

### Install requirements ###
```bash
cd cloudyweb
pip install -r requirements/dev.txt
```

### Sync database ###
```bash
python manage.py migrate
```

## Running ##
```bash
python manage.py runserver 0.0.0.0:8000
```

Open browser to http://127.0.0.1:8000


## Testing Locally ##
```bash
python manage.py test
```


## API Usage ##
### Account ###
##### 1. Create User (Activation Email will be sent over the email) #####
    $ curl -X POST http://127.0.0.1:8000/api-token-auth/registrations/ --data "email=john@doe.com&username=john&password=doe"
    ==> {"username":"john","email":"","first_name":"","last_name":""}

##### 2. Retrieving Token #####
    $ curl -X POST http://127.0.0.1:8000/api-token-auth/tokens/ --data "username=john&password=doe"
    ==> {"token":"7f1334b4b27202afe8ef3e078dfc849291e908b9"}

##### 3. Retrieving User Resources #####
    $ curl -X GET http://127.0.0.1:8000/users/ -H 'Authorization: Token abcdefghijklmnopqrstuvwxyz123456790'
    ==> [{"username":"john","email":"","first_name":"","last_name":""}, ...]

### CloudyGames ###
##### 1. Games #####
  * Create Games
    * request method: POST
    *  url: '/games/'
    * data: {'name': 'game1', 'publisher': 'pub1', 'max_limit': 4, 'address': 'http://0.0.0.0', 'description': '', 'thumbnail':''}
    * access right: operator only
  * Read Games
    * request method: GET
    * url:
      * '/games/'
      * '/games/4/' where 4 is game__id
      * '/games/?owned=1' to get owned games (0 to get all)
      * '/games/?name=game4&id=1&publisher=pub1'
    * access right: available for all
    * returns {'id', 'name', 'publisher', 'max_limit', 'address', 'description', 'thumbnail'}
  * Update Games
    * request method: PATCH
    * url: '/games/3/' where 3 is game__id
    * data: {} data that you want to update only, refer to create games
    * access right: operator only
 * Delete Games
    * request method: DELETE
    * url: '/games/3/' where 3 is game__id
    * access right: operator only
##### 2. Game Ownership #####
  * Add Game to "My Collection"
      * request method: POST
      * url: '/game-ownership/'
      * data: {'game': '1', 'user': 'john'} where game is game__id and user is user__name
      * access right: operator or their own
  * Read Game Ownership
    * request method: GET
    * url:
      * '/game-ownership/'
      * '/game-ownership/?user=user1'
      * '/game-ownership/?game=1'
      * '/game-ownership/3/' where 3 is game-ownership__id
     * access right: operator or their own
     * returns {'id', 'user', 'game'}
  * Delete Game Ownership
    * request method: DELETE
    * url: '/game-ownership/3/' where 3 is game-ownership__id
    * access right: operator or their own
##### 3. Game Session #####
  * Join Game
    * request method: POST
    * url: '/game-session/'
    * data: {'user': 'user1', 'game': '1'}
    * access right: operator or their own
  * Read Game Session
    * request method: GET
    * url:
      * '/game-session/'
      * '/game-session/4/' were 4 is game-session__id
      * '/game-session/?user=user1'
      * '/game-session/?game=3'
    * access right: operator or their own
    * returns {'id', 'user', 'game', 'controller', 'streaming_port'}
  * Quit Game
    * request method: DELETE
    * url: '/game-session/3/'
     * access right: operator or their own
##### 4. Save Data #####
  * Create or Update Save Data
    * request method: POST
    * url: '/save-data/'
    * data: {'saved_file': '', 'game': '1', 'user': 'user1'}
    * access right: operator or their own
  * Read Save Data
    * request method: GET
    * url:
      * '/save-data/'
      * '/save-data/4/'
      * '/games/?game=1'
      * '/games/?user=user1'
    * access right: operator or their own
    * returns {'id', 'saved_file', 'user', 'game'}
  * Delete Save Data
    * request method: DELETE
    * url: '/save-data/3/'
    * access right: operator or their own

## List of Resources

* `/users/`
* '/games/'
* '/game-ownership/'
* '/game-session/'
* '/save-data/'
