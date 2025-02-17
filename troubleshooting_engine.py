class TroubleshootingEngine:
    def __init__(self, device_state, command_parser, ssh_connector):
        self.device_state = device_state
        self.command_parser = command_parser
        self.ssh_connector = ssh_connector

    def diagnose_interface_issues(self, interface):
        interface_state = self.device_state.get_interface_state(interface)

        if not interface_state:
            return f"Interface {interface} not found in device state."

        if interface_state['status'] == 'down' and interface_state['protocol'] == 'down':
            return f"Interface {interface} is down. Check physical connection, cabling, and shutdown state."
        elif interface_state['status'] == 'up' and interface_state['protocol'] == 'down':
            return f"Interface {interface} is up, but the protocol is down. Check routing, ACLs, and other configuration."
        else:
            return f"Interface {interface} is up and functioning normally."

    def check_connectivity(self, destination_ip):
        ping_command = f"ping {destination_ip} source {self.device_state.ip_address}"
        output = self.ssh_connector.send_command(ping_command)

        if "Success rate is 0 percent" in output:
            return f"Connectivity to {destination_ip} is failing.  Check routing, ACLs, and firewall rules."
        else:
            return f"Connectivity to {destination_ip} appears to be working."

    def attempt_recovery(self, issue, interface=None):
        if "interface is down" in issue.lower():
            command = self.command_parser.format_command("configure_interface_noshutdown", {'interface':interface})
            if command:
                output = self.ssh_connector.send_command(command)
                if "Invalid input detected" in output:
                    return "Error enabling interface. Review command."
            return "Attempted to bring the interface up."
        else:
            return "Recovery not implemented for this issue."