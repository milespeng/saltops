send_file:
  file.managed:
      - name: /tmp/elasticsearch-2.3.5.tar.gz
      - source: salt://files/elasticsearch-2.3.5.tar.gz

extract_file:
  cmd.run:
      - name: tar -xvf ./elasticsearch-2.3.5.tar.gz
      - cwd: /tmp
      - unless: test -d /tmp/elasticsearch-2.3.5
      - require:
        - file: send_file

run_es:
  cmd.run:
      - cwd: /tmp/elasticsearch-2.3.5/bin
      - name: ./elasticsearch -d
      - user: kira
      - unless: test -d /tmp/elasticsearch-2.3.5