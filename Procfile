web: gunicorn seiyonnet.wsgi --log-file -
web: gunicorn publish_test.wsgi --log-file -
python manage.py collectstatic --noinput
manage.py migrate