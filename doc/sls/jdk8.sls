jdk.send_file:
  file.managed:
      - name: /tmp/jdk-${version}-linux-x64.tar.gz
      - source: salt://jdk/files/jdk-${version}-linux-x64.tar.gz

jdk.extract_file:
  cmd.run:
      - name: tar -xvf ./jdk-${version}-linux-x64.tar.gz
      - cwd: /tmp
      - unless: test -d /tmp/jdk${version}
      - require:
        - file: jdk.send_file

jdk.make_java_dir:
  cmd.run:
      - name: mkdir -p /opt/jdk
      - unless: test -d /opt/jdk/
      - require:
        - cmd: jdk.extract_file

jdk.move_java:
  cmd.run:
      - name: mv /tmp/jdk${version} /opt/jdk
      - unless: test -d /opt/jdk/jdk${version}
      - require:
        - cmd: jdk.make_java_dir

jdk.change_env:
  cmd.run:
      - name: echo 'export JAVA_HOME=/opt/jdk/jdk${version}  \n export PATH=$JAVA_HOME/bin:$PATH \n export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar \n' >> /etc/profile
      - user: root
      - unless: cat /etc/profile|grep JAVA
      - require:
        - cmd: jdk.move_java