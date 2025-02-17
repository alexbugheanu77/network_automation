class DeviceState:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.interfaces = {}
        self.vlans = {}
        self.routing_table = {}
        self.ospf_neighbors = {}
        self.config = {}

    def update_interface_state(self, interface, ip_address, status, protocol):
        self.interfaces[interface] = {
            'ip_address': ip_address,
            'status': status,
            'protocol': protocol
        }

    def get_interface_state(self, interface):
        return self.interfaces.get(interface)

    def update_running_config(self, config_output):
        self.config = config_output

    def get_running_config(self):
        return self.config

    def __str__(self):
        return f"Device State for {self.ip_address}:\nInterfaces: {self.interfaces}\nConfig: {self.config[:200]}..."