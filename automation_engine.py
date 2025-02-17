class AutomationEngine:
    def __init__(self, device_state, command_parser, ssh_connector):
        self.device_state = device_state
        self.command_parser = command_parser
        self.ssh_connector = ssh_connector

    def execute_workflow(self, workflow_name, params=None):
        if workflow_name == "backup_config":
            show_run_command = self.command_parser.format_command("show_config")
            config = self.ssh_connector.send_command(show_run_command)

            with open(self.device_state.ip_address + "_config_backup.txt", "w") as f:
                f.write(config)

            return "Configuration backup completed."
        elif workflow_name == "configure_vlan":
            if not params or 'vlan_id' not in params or 'vlan_name' not in params:
                return "Missing VLAN parameters."

            vlan_id = params['vlan_id']
            vlan_name = params['vlan_name']

            commands = [
                "configure terminal",
                f"vlan {vlan_id}",
                f"name {vlan_name}",
                "end"
            ]
            for command in commands:
              config_commands = self.command_parser.format_command("configure_vlan_basic", commands)
              output = self.ssh_connector.send_command(command)

            return f"VLAN {vlan_id} configured with name {vlan_name}."
        else:
            return "Workflow not found."