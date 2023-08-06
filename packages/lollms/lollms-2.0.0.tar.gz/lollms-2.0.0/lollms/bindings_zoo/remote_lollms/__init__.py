######
# Project       : lollms
# File          : binding.py
# Author        : ParisNeo with the help of the community
# Underlying binding : ParisNeo's lollms remote service
# Supported by Nomic-AI
# license       : Apache 2.0
# Description   : 
# This is an interface class for lollms bindings.

# This binding is a wrapper to open ai's api

######
from pathlib import Path
from typing import Callable
from lollms.config import BaseConfig, TypedConfig, ConfigTemplate, InstallOption
from lollms.paths import LollmsPaths
from lollms.binding import LLMBinding, LOLLMSConfig
from lollms.helpers import ASCIIColors
from lollms.types import MSG_TYPE
import subprocess
import yaml
import re

import time
import requests
import socketio

__author__ = "parisneo"
__github__ = "https://github.com/ParisNeo/lollms_bindings_zoo"
__copyright__ = "Copyright 2023, "
__license__ = "Apache 2.0"

binding_name = "LoLLMs"
binding_folder_name = ""

class LoLLMs(LLMBinding):
    # Define what is the extension of the model files supported by your binding
    # Only applicable for local models for remote models like gpt4 and others, you can keep it empty 
    # and reimplement your own list_models method
    file_extension='*.bin' 
    def __init__(self, 
                config: LOLLMSConfig, 
                lollms_paths: LollmsPaths = LollmsPaths(), 
                installation_option:InstallOption=InstallOption.INSTALL_IF_NECESSARY
                ) -> None:
        """
        Initialize the Binding.

        Args:
            config (LOLLMSConfig): The configuration object for LOLLMS.
            lollms_paths (LollmsPaths, optional): The paths object for LOLLMS. Defaults to LollmsPaths().
            installation_option (InstallOption, optional): The installation option for LOLLMS. Defaults to InstallOption.INSTALL_IF_NECESSARY.
        """
        # Initialization code goes here

        binding_config = TypedConfig(
            ConfigTemplate(
            [
                {"name":"servers_addresses","type":"list","value":[], "help":"A list of server addresses for example ['http://localhost:9601', 'http://localhost:9602']"},
                {"name":"keep_only_active_servers","type":"bool","value":True, "help":"If true, then only active servers will be kept in the loop"},
            ]
            ),
            BaseConfig(config={
                "servers_addresses"         : [],    # list of hosts to be used
                "keep_only_active_servers"  : True   # if true only keep actiave servers in the list
            })
        )
        super().__init__(
                            Path(__file__).parent, 
                            lollms_paths, 
                            config, 
                            binding_config, 
                            installation_option
                        )
        
    def build_model(self):
        # Create two lists to hold active and inactive servers
        self.servers_addresses = self.binding_config.config.servers_addresses
        active_servers = []
        inactive_servers = []

        # Ping servers
        for server_url in self.servers_addresses:
            try:
                # Create a Socket.IO client instance
                sio = socketio.Client()

                # Define the event handler for the 'connect' event
                @sio.event
                def connect():
                    pass

                # Define the event handler for the 'disconnect' event
                @sio.event
                def disconnect():
                    pass

                # Connect to the server
                sio.connect(server_url)

                # Disconnect from the server
                sio.disconnect()
                active_servers.append(server_url)  # Add active server to the list
                ASCIIColors.green(f"Server : {server_url} is active")
            except:
                inactive_servers.append(server_url)  # Add inactive server to the list
                ASCIIColors.error(f"Server : {server_url} is unreachable")
        # Do your initialization stuff
        if self.binding_config.config["keep_only_active_servers"]:
            self.servers_addresses = active_servers
        return self

    def install(self):
        super().install()
        requirements_file = self.binding_dir / "requirements.txt"
        # install requirements
        subprocess.run(["pip", "install", "--upgrade", "--no-cache-dir", "-r", str(requirements_file)])
        ASCIIColors.success("Installed successfully")

    def tokenize(self, prompt:str):
        """
        Tokenizes the given prompt using the model's tokenizer.

        Args:
            prompt (str): The input prompt to be tokenized.

        Returns:
            list: A list of tokens representing the tokenized prompt.
        """
        # Split text into words while preserving spaces
        words = re.findall(r'\w+|\s+', prompt)
        return words

    def detokenize(self, tokens_list:list):
        """
        Detokenizes the given list of tokens using the model's tokenizer.

        Args:
            tokens_list (list): A list of tokens to be detokenized.

        Returns:
            str: The detokenized text as a string.
        """
        return "".join(tokens_list)
    
    def generate(self, 
                 prompt:str,                  
                 n_predict: int = 128,
                 callback: Callable[[str], None] = bool,
                 verbose: bool = False,
                 **gpt_params ):
        """Generates text out of a prompt

        Args:
            prompt (str): The prompt to use for generation
            n_predict (int, optional): Number of tokens to prodict. Defaults to 128.
            callback (Callable[[str], None], optional): A callback function that is called everytime a new text element is generated. Defaults to None.
            verbose (bool, optional): If true, the code will spit many informations about the generation process. Defaults to False.
        """
        infos = {
            "generated":False,
            "found": False,
            "generated_text":""
        }
        index = 0
        while True:
            try:
                server_url = self.servers_addresses[index]
                # Create a Socket.IO client instance
                sio = socketio.Client()
                # Event handler for successful connection
                @sio.event
                def connect():
                    infos["found"]= True
                    if prompt:
                        # Trigger the 'generate_text' event with the prompt
                        sio.emit('generate_text', {'prompt': prompt, 'personality':-1, "n_predicts":n_predict})

                @sio.event
                def text_chunk(data):
                    if callback is not None:
                        if not callback(data["chunk"], MSG_TYPE(data["type"])):
                            sio.emit()

                @sio.event
                def text_generated(data):
                    infos["generated_text"]=data["text"]
                    sio.disconnect()

                @sio.event
                def buzzy():
                    #works but not ready We need to wait
                    sio.disconnect()

                # Connect to the Socket.IO server
                sio.connect(server_url)

                # Start the event loop
                sio.wait()
                infos["generated"] = True
                break
            except Exception as ex:
                index +=1
                if index>=len(self.servers_addresses) and not infos["found"]:
                    break
                if index>=len(self.servers_addresses):
                    # Wait 1 second and retry again
                    time.sleep(1)
                    index = 0
        if not infos["found"]:
            ASCIIColors.error("No server was ready to receive this request")
        return infos["generated_text"]
    
    @staticmethod
    def list_models(config:dict):
        """Lists the models for this binding
        """
        binding_path = Path(__file__).parent
        file_path = binding_path/"models.yaml"

        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        return yaml_data
                
    @staticmethod
    def get_available_models():
        # Create the file path relative to the child class's directory
        binding_path = Path(__file__).parent
        file_path = binding_path/"models.yaml"

        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        return yaml_data