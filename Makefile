run:
	python manage.py runserver 0.0.0.0:8000

prod:
	gunicorn cloudyweb.wsgi -b 127.0.0.1:8000 --pid /tmp/gunicorn.pid --daemon
