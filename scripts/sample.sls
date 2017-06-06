{% set tomcat = "apache-tomcat-8.5.15.zip" %}
{% set tomcat_dir = "apache-tomcat-8.5.15" %}
{% set current_path = salt['environ.get']('PATH', '/bin:/usr/bin') %}
rm_file:
  file.managed:
      - name: /tmp/{{tomcat}}
      - unless: test -f /tmp/{{tomcat}}
      - source: salt://{{tomcat}}

extract_file:
  cmd.run:
      - name: unzip -o ./{{tomcat}}
      - cwd: /tmp
      - unless: test -d /tmp/{{tomcat}}
      - require:
          - file: send_file

move_file:
  cmd.run:
      - name: mv ./{{tomcat_dir}} /opt
      - cwd: /tmp
      - unless: test -d /tmp/{{tomcat_dir}}
      - require:
          - cmd: extract_file

chmod_file:
  cmd.run:
      - name: chmod -Rf 777 /opt/{{tomcat_dir}}/bin
      - cwd: /opt
      - unless: test -d /opt/{{tomcat_dir}}
      - require:
          - cmd: move_file


run_tomcat:
  cmd.run:
      - cwd: /opt/{{tomcat_dir}}/bin
      - name: ./startup.sh
      - env:
         - BATCH: 'yes'
         - JAVA_HOME: "/opt/jdk/jdk1.8.0_131"
      - require:
          - cmd: chmod_file
