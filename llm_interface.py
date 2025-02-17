import openai
import os

class LLMInterface:
    def __init__(self, model="gpt-3.5-turbo"):  # Or gpt-4, etc.
        self.model = model
        # Use environment variables to store the API key
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables. Please set the OPENAI_API_KEY environment variable.")

    def generate_response(self, prompt):
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful network automation assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message['content']
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return None

    def interpret_intent(self, natural_language_query, device_state, command_parser):
        # Craft a prompt to guide the LLM
        prompt = f"""
        You are a network automation assistant helping to manage a Cisco network device.
        The device is running {command_parser.device_type}.
        Here is the device's current state: {device_state}

        The user is asking the following: {natural_language_query}

        Based on this request, you should determine:
        1. The 'intent' of the user (e.g., 'show_interfaces', 'configure_interface_ip', 'check_connectivity', 'backup_config').
        2. Any required 'parameters' for the intent (e.g., interface name, IP address, VLAN ID).
        3. If the intent is unknown or cannot be safely determined return "unknown".

        Return your response as a JSON-like dictionary with the keys "intent" and "parameters".
        For example:
        {{"intent": "show_interfaces", "parameters": null}}
        {{"intent": "configure_interface_ip", "parameters": {{"interface": "GigabitEthernet0/1", "ip_address": "10.0.0.1", "netmask": "255.255.255.0"}}}}
        """
        llm_response = self.generate_response(prompt)
        return llm_response

# Example Usage (remove from file, use in main.py for testing)
# llm = LLMInterface()
# natural_language_query = "Show me the interfaces on the router"
# llm_response = llm.interpret_intent(natural_language_query, device_state, command_parser)
# print(llm_response)  # {"intent": "show_interfaces", "parameters": null}