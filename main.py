import device_list
from ssh_connector import SSHConnector
from command_parser import CommandParser
from device_state import DeviceState
from troubleshooting_engine import TroubleshootingEngine
from automation_engine import AutomationEngine
from llm_interface import LLMInterface
import json #For parsing LLM output

if __name__ == "__main__":
    # Load device list
    for device_config in device_list.devices:
        # Initialize components for each device
        ssh_conn = SSHConnector(device_config)
        parser = CommandParser(device_config["device_type"])
        device_state = DeviceState(device_config["ip"])
        troubleshooter = TroubleshootingEngine(device_state, parser, ssh_conn)
        automation = AutomationEngine(device_state, parser, ssh_conn)
        llm = LLMInterface()

        # Connect to the device
        if ssh_conn.connect():
            while True:
                user_input = input(f"Enter command for {device_config['ip']} (or 'exit'): ")
                if user_input.lower() == "exit":
                    break

                # Use LLM to interpret the intent
                llm_response = llm.interpret_intent(user_input, device_state, parser)
                print("LLM Response:", llm_response)  #Print full LLM response for debugging
                try:
                    llm_data = json.loads(llm_response)  #Parse the JSON
                    intent = llm_data.get("intent") #Get intent
                    params = llm_data.get("parameters") #Get parameters
                except json.JSONDecodeError as e:
                    print(f"Error decoding LLM response: {e}")
                    intent = None
                    params = None

                if intent:
                    # Format the command
                    command = parser.format_command(intent, params)

                    if command:
                        # Send the command to the device
                        output = ssh_conn.send_command(command)
                        print("Device Output:\n", output)

                        # Parse the output and update device state
                        if "show ip interface brief" in command:
                            interface_data = parser.parse_output("show ip interface brief", output)
                            if interface_data:
                                for intf in interface_data:
                                    device_state.update_interface_state(intf['interface'], intf['ip_address'], intf['status'], intf['protocol'])
                                    print(troubleshooter.diagnose_interface_issues(intf['interface']))
                        elif "show running-config" in command:
                            config = parser.parse_output("show running-config", output)
                            device_state.update_running_config(config)
                            #print (device_state.get_running_config())
                        # Add other parsing and state updating as needed
                        elif "backup_config" in intent: #Use intent not command
                            result = automation.execute_workflow("backup_config")
                            print(result)

                    else:
                        print("Command could not be formatted.")
                else:
                    print("Intent not recognized by LLM or parsing error.")

            # Disconnect
            ssh_conn.disconnect()