run:
	python manage.py collectstatic --no-input
	python manage.py migrate auth --noinput
	python manage.py migrate movies --fake --noinput
	python manage.py migrate --noinput
	python sqlite_to_postgres/load_data.py sqlite_to_postgres/db.sqlite
	python manage.py createsuperuser --username admin --email admin@example.com
