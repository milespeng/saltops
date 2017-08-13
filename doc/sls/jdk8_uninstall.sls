rm_tmp_jdk_tar:
  cmd.run:
      - name: rm -Rf ./jdk-${version}-linux-x64.tar.gz
      - cwd: /tmp
      - unless: test -d /tmp/jdk-${version}-linux-x64.tar.gz

rm_jdk:
  cmd.run:
      - name: rm -Rf /opt/jdk
      - unless: test -d /opt/jdk

rm_javahome_profile:
  cmd.run:
      - name: sed -i '/JAVA_HOME/d' /etc/profile
