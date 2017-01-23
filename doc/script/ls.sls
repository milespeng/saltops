send_file:
    file.managed:
        - name: /tmp/apr.tar
        - source: salt://files/apr.tar
        - mode: 777

tar_file:
  cmd.run:
      - cwd: /tmp/
      - name: tar -xvf ./apr.tar