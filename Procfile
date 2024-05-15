web: gunicorn PacilFix.wsgi --log-file -
#or works good with external database
web: python manage.py migrate && gunicorn PacilFix.wsgi