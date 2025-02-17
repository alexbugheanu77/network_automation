# Add to your web_ui.py file
from flask import Flask, render_template, request
import device_list
from ssh_connector import SSHConnector
from command_parser import CommandParser
from device_state import DeviceState
from troubleshooting_engine import TroubleshootingEngine
from automation_engine import AutomationEngine
from llm_interface import LLMInterface
import json  # For parsing LLM output
import os
# Before app = Flask(__name__)
try:
    llm = LLMInterface()  # Initialize after setting the API key
except ValueError as e:
    print(f"Error initializing LLM: {e}")
    # Handle the error appropriately - exit, disable LLM functionality, etc.
    exit() #Example exit