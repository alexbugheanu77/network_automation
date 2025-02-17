import netmiko
from netmiko import ConnectHandler

class SSHConnector:
    def __init__(self, device_config):  # Takes a device dictionary
        self.ip = device_config["ip"]
        self.username = device_config["username"]
        self.password = device_config["password"]
        self.device_type = device_config["device_type"]
        self.connection = None

    def connect(self):
        try:
            self.connection = ConnectHandler(
                device_type=self.device_type,
                host=self.ip,
                username=self.username,
                password=self.password,
                global_delay_factor=1
            )
            print(f"Successfully connected to {self.ip}")
            return True
        except Exception as e:
            print(f"Error connecting to {self.ip}: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.disconnect()
            print(f"Disconnected from {self.ip}")
        else:
            print("Not connected.")

    def send_command(self, command):
        if self.connection:
            try:
                output = self.connection.send_command(command)
                return output
            except Exception as e:
                print(f"Error sending command: {e}")
                return None
        else:
            print("Not connected. Please connect first.")
            return None