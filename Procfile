web: gunicorn final.wsgi --log-file -

web: python manage.py migrate && gunicorn final.wsgi