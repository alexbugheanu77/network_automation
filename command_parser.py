import re

class CommandParser:
    def __init__(self, device_type='cisco_ios'):
        self.device_type = device_type

    def format_command(self, intent, params=None):
        if self.device_type == 'cisco_ios':
            if intent == "show_interfaces":
                return "show ip interface brief"
            elif intent == "show_version":
                return "show version"
            elif intent == "show_config":
                return "show running-config"
            elif intent == "configure_interface_ip":
                interface = params['interface']
                ip_address = params['ip_address']
                netmask = params['netmask']
                config_commands = [
                    "configure terminal",
                    f"interface {interface}",
                    f"ip address {ip_address} {netmask}",
                    "no shutdown",
                    "end"
                ]
                return "\n".join(config_commands)
            elif intent == "configure_interface_noshutdown":
                interface = params['interface']
                config_commands = [
                        "configure terminal",
                        f"interface {interface}",
                        "no shutdown",
                        "end"
                    ]
                return "\n".join(config_commands)
            else:
                return None
        elif self.device_type == 'cisco_nxos':
            # Implement NX-OS command mappings here
            pass
        else:
            return None

    def parse_output(self, command, output):
        if command == "show ip interface brief":
            interfaces = []
            lines = output.splitlines()
            for line in lines[1:]:
                match = re.match(r'(\S+)\s+(\S+)\s+(\S+)\s+([\w\.]+)\s+(\w+)\s+(\w+)', line)
                if match:
                    intf, ip_address, mask, status, protocol = match.groups()
                    interfaces.append({
                        "interface": intf,
                        "ip_address": ip_address,
                        "status": status,
                        "protocol": protocol
                    })
            return interfaces
        elif command == "show version":
            version_info = {}
            lines = output.splitlines()
            for line in lines:
                if "Cisco IOS Software" in line:
                    version_info["ios_version"] = line.split("Version ")[1].split(",")[0]
                if "uptime" in line:
                    version_info["uptime"] = line.split("uptime is ")[1]
            return version_info
        elif command == "show running-config":
            config_info = {}
            # Parse the running configuration
            return config_info
        else:
            return output