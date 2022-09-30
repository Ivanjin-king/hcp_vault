import paramiko
import keyring
import time
import subprocess
#from paramiko.ssh_exception import SSHException
t=time.time()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hostname = ["x.x.x.x"]
username = "root"
pwd = keyring.get_password("agt_test", "root")
for host in hostname:
    send_command = subprocess.check_output(["ssh-copy-id", f"{username}@{host}"])
    send_command = subprocess.check_output([f"{pwd}"])
    return_result = send_command.decode()
    print(return_result)

def ssh_verify():
    ssh.connect(hostname=host, username=username, password=pwd)
    session = ssh.get_transport().open_session()
    session.invoke_shell()
    command = f"ssh-copy-id {username}@{host}\n"
    session.sendall(command)
    output = str(session.recv(1024), encoding="utf-8")
    print("output: ", output)
    ssh.close()
print(time.time()-t)