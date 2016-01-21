# CloudyWeb

Cloudyweb is
- CloudyPanel: administration panel for operator
- CloudyService: web service for client


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
