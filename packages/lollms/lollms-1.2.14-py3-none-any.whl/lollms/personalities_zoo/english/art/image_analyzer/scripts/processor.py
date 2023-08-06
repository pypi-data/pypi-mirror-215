import subprocess
from pathlib import Path
import os
import sys
from lollms.personality import APScript, AIPersonality, MSG_TYPE
import time
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent))
import torch
from torchvision import transforms
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
   
class Processor(APScript):
    """
    A class that processes model inputs and outputs.

    Inherits from APScript.
    """

    def __init__(self, personality: AIPersonality) -> None:
        super().__init__()
        self.personality=personality
        print("Preparing Image Analyzer. Please Stand by")
        self.personality = personality
        self.word_callback = None
        self.generate_fn = None
        self.config = self.load_config_file(self.personality.lollms_paths.personal_configuration_path / 'personality_image_analyzer_config.yaml')
        self.device = self.config["device"]

        self.model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b")
        self.processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")



    def add_file(self, path):
        try:
            # only one path is required
            self.raw_image = Image.open(path).convert('RGB')
            self.files = [path]
            inputs = self.processor(self.raw_image, return_tensors="pt").to(self.device) #"cuda")
            def callback(output):
                token = output.argmax(dim=-1)
                token_str = self.processor.decode(token)
                print(token_str, end='')
            print("Processing...")
            output = self.processor.decode(self.model.generate(**inputs, max_new_tokens=self.personality.model_n_predicts)[0], skip_special_tokens=True, callback=callback)
            print("Image description: "+output)
            return True
        except:
            print("Couoldn't load file. PLease check the profided path.")
            return False

    def remove_file(self, path):
        # only one path is required
        self.files = []

    def remove_text_from_string(self, string, text_to_find):
        """
        Removes everything from the first occurrence of the specified text in the string (case-insensitive).

        Parameters:
        string (str): The original string.
        text_to_find (str): The text to find in the string.

        Returns:
        str: The updated string.
        """
        index = string.lower().find(text_to_find.lower())

        if index != -1:
            string = string[:index]

        return string
    
    def process(self, text):
        bot_says = self.bot_says + text
        antiprompt = self.personality.detect_antiprompt(bot_says)
        if antiprompt:
            self.bot_says = self.remove_text_from_string(bot_says,antiprompt)
            print("Detected hallucination")
            return False
        else:
            self.bot_says = bot_says
            return True

    def generate(self, prompt, max_size):
        self.bot_says = ""
        return self.personality.model.generate(
                                prompt, 
                                max_size, 
                                self.process,
                                temperature=self.personality.model_temperature,
                                top_k=self.personality.model_top_k,
                                top_p=self.personality.model_top_p,
                                repeat_penalty=self.personality.model_repeat_penalty,
                                ).strip()    
        

    def run_workflow(self, prompt, previous_discussion_text="", callback=None):
        """
        Runs the workflow for processing the model input and output.

        This method should be called to execute the processing workflow.

        Args:
            generate_fn (function): A function that generates model output based on the input prompt.
                The function should take a single argument (prompt) and return the generated text.
            prompt (str): The input prompt for the model.
            previous_discussion_text (str, optional): The text of the previous discussion. Default is an empty string.
            callback a callback function that gets called each time a new token is received
        Returns:
            None
        """
        self.word_callback = callback
        try:
            inputs = self.processor(self.raw_image, f"{previous_discussion_text}{self.personality.link_text}{self.personality.ai_message_prefix}", return_tensors="pt").to(self.device) #"cuda")
            def local_callback(output):
                token = output.argmax(dim=-1)
                token_str = self.processor.decode(token)
                if callback is not None:
                    callback(token_str, MSG_TYPE.MSG_TYPE_CHUNK)
                else:
                    print(token_str, end='')


            output = self.processor.decode(self.model.generate(**inputs, max_new_tokens=self.personality.model_n_predicts)[0], skip_special_tokens=True, callback=local_callback)
        except Exception as ex:
            print(ex)
            output = "There seems to be a problem with your image, please upload a valid image to talk about"
        return output


