#!/usr/bin/python2.7
import socket
HOST = '0.0.0.0'
PORT = 113
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((HOST,PORT))
server_socket.listen(5)
client_socket,(client_ip,client_port) = server_socket.accept()
while True:
     #command = raw_input("postgres")
     #client_socket.send(command)

     data = client_socket.recv(1024).decode()
     if not len(data) > 0:
        break
     print(data.decode())
     one = data.split('\r\n')
     print (one)
     data = one[0]+ " : USERID : UNIX : gadmin" + "\r\n"
     print(data)
     client_socket.send(data.encode())
     break
client_socket.close()