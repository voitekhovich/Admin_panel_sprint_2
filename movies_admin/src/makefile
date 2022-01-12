run:
	python manage.py collectstatic --no-input
	python manage.py makemigrations --noinput
	python manage.py migrate --noinput
	python sqlite_to_postgres/load_data.py sqlite_to_postgres/db.sqlite
	python manage.py createsuperuser --username admin --email admin@example.com
