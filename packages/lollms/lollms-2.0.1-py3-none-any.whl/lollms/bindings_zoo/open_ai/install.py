import subprocess
from pathlib import Path
from lollms.binding import LOLLMSConfig, BindingInstaller
from lollms.helpers import ASCIIColors
import yaml

class Install(BindingInstaller):
    def __init__(self, config:LOLLMSConfig=None, force_reinstall=False):
        # Build parent
        super().__init__(config)
        # Get the current directory
        current_dir = Path(__file__).resolve().parent
        install_file = current_dir / ".installed"

        if not install_file.exists() or force_reinstall:
            ASCIIColors.info("-------------- OpenAI Binding -------------------------------")
            print("This is the first time you are using this binding.")
            print("Installing ...")
            # Step 2: Install dependencies using pip from requirements.txt
            requirements_file = current_dir / "requirements.txt"
            subprocess.run(["pip", "install", "--upgrade", "--no-cache-dir", "-r", str(requirements_file)])

            # Create the models folder
            models_folder = config.lollms_paths.personal_models_path/f"{Path(__file__).parent.stem}"
            models_folder.mkdir(exist_ok=True, parents=True)

            #Create 
            self._local_config_file_path = Path(__file__).parent/"local_config.yaml"
            if not self._local_config_file_path.exists():
                ASCIIColors.error("----------------------")
                ASCIIColors.error("Attention please")
                ASCIIColors.error("----------------------")
                ASCIIColors.error("The chatgpt binding uses the openai API which is a paid service. Please create an account on the openAi website (https://platform.openai.com/) then generate a key and provide it here.")
                key = input("Please enter your Open AI Key:")
                config={
                    "openai_key":key
                }
                binding_config_path = config.lollms_paths.personal_configuration_path / "binding_open_ai_config.yaml"
                self.create_config_file(config, binding_config_path)
            #Create the install file (a file that is used to insure the installation was done correctly)
            with open(install_file,"w") as f:
                f.write("ok")
            print("Installed successfully")
            

    def create_config_file(self, config, path):
        """
        Create a local_config.yaml file with predefined data.

        The function creates a local_config.yaml file with the specified data. The file is saved in the parent directory
        of the current file.

        Args:
            None

        Returns:
            None
        """
        with open(path, 'w') as file:
            yaml.dump(config, file)