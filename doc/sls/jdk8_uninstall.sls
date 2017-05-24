rm_tmpjdk:
  cmd.run:
      - name: rm -Rf ./jdk-${version}-linux-x64.tar.gz
      - cwd: /tmp

rm_jdk:
  cmd.run:
      - name: rm -Rf /opt/jdk

rm_javahome_profile:
  cmd.run:
      - name: sed -i '/JAVA/d' /etc/profile

rm_classpath_profile:
  cmd.run:
      - name: sed -i '/CLASSPATH/d' /etc/profile