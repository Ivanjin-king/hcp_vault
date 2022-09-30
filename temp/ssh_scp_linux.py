import paramiko
import keyring
import time
import subprocess
"""Client to handle connections and actions executed against a remote host."""
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException
#from .log import logging
import logging
import os

class RemoteClient():
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, host, user,password, ssh_key_filepath):
        self.host = host
        self.user = user
        self.password = password
        self.ssh_key_filepath = ssh_key_filepath
        self.client = None
        #self.remote_path = remote_path
        self._get_ssh_key()
        self._upload_ssh_key()

    def _get_ssh_key(self):
        """ Fetch locally stored SSH key."""

        try:
            self.ssh_key = RSAKey.from_private_key_file(
                self.ssh_key_filepath
            )

            logging.info(
                f"Found SSH key at self {self.ssh_key_filepath}"
            )

            return self.ssh_key
        except SSHException as e:
            logging.error(e)

    def _upload_ssh_key(self):
        try:
            print("test")
            os.system(
                f"ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.host}"
            )
            print("test")
            logging.info(f"{self.ssh_key_filepath} uploaded to {self.host}")
        except FileNotFoundError as error:
            logging.error(error)

logging.basicConfig(filename='log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

home_directory =os.path.expanduser('~')
host = "x.x.x.x"
user = "root"
password ="xxx"
ssh_key_filepath = f"{home_directory}/.ssh/id_rsa"
home_directory =os.path.expanduser('~')
f = RemoteClient(host,user,password,ssh_key_filepath)

logging.info(
                f"Found SSH key at self {ssh_key_filepath}"
            )

