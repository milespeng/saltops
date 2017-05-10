docker run -i -t -d -p 8001:8000 -p 4505:4505 -p 4506:4506 hub.c.163.com/cc8565/saltops /opt/saltops/docker_start.sh && python3 /opt/saltops/manage.py runserver 0.0.0.0:8000

docker pull hub.c.163.com/cc8565/saltops