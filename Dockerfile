FROM ubuntu
MAINTAINER wuwenhao

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y git
RUN apt-get install -y vim
RUN wget -O - https://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
RUN touch /etc/apt/sources.list.d/saltstack.list
RUN echo 'deb http://repo.saltstack.com/apt/ubuntu/14.04/amd64/latest trusty main' > /etc/apt/sources.list.d/saltstack.list

RUN apt-get update
RUN apt-get install -y salt-master
RUN apt-get install -y salt-minion
RUN apt-get install -y salt-api
RUN apt-get install -y python3-pip

RUN echo  'auto_accept: True'>> /etc/salt/master
RUN echo  'file_roots:'>> /etc/salt/master
RUN echo  '    base:'>> /etc/salt/master
RUN echo  '        - /srv/salt/' >> /etc/salt/master
RUN echo  'rest_cherrypy:' >> /etc/salt/master
RUN echo  '    port: 8001' >> /etc/salt/master
RUN echo  '    debug: True' >> /etc/salt/master
RUN echo  '    ssl_crt: /etc/pki/tls/certs/localhost.crt' >> /etc/salt/master
RUN echo  '    ssl_key: /etc/pki/tls/certs/localhost.key' >> /etc/salt/master
RUN echo  '    disable_ssl: True' >> /etc/salt/master
RUN echo  'external_auth:' >> /etc/salt/master
RUN echo  '    pam:' >> /etc/salt/master
RUN echo  '        saltops:' >> /etc/salt/master
RUN echo  "            - .*" >> /etc/salt/master
RUN echo  "            - '@wheel' " >> /etc/salt/master
RUN echo  "            - '@runner'" >> /etc/salt/master
RUN echo  "master: 127.0.0.1">>/etc/salt/minion
RUN mkdir -p /srv/salt

WORKDIR /opt/
RUN git clone https://git.oschina.net/wuwenhao/saltops.git
WORKDIR /opt/saltops/
RUN cp -f /opt/saltops/saltops/settings_backup.py /opt/saltops/saltops/settings.py
RUN pip3 install -r ./requiement.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN useradd -ms /bin/bash saltops
RUN echo 'saltops:saltops' | chpasswd
RUN chmod 777 /opt/saltops/docker_start.sh



