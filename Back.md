docker run -i -t -d -p 8001:8000 -p 4505:4505 -p 4506:4506 hub.c.163.com/cc8565/saltops
 
 
 /opt/saltops/docker_start.sh

docker pull hub.c.163.com/cc8565/saltops

# 使用Docker部署

    docker pull hub.c.163.com/cc8565/saltops
    docker run -i -t -d -p 8001:8000 -p 4505:4505 -p 4506:4506 hub.c.163.com/cc8565/saltops

docker-enter进去容器，然后执行

     /opt/saltops/docker_start.sh
