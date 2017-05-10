service salt-master start
service salt-minion start
service salt-api start
python3 /opt/saltops/manage.py runserver 0.0.0.0:8000

