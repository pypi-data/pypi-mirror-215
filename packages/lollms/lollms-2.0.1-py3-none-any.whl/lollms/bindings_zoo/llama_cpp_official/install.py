import subprocess, os
from pathlib import Path
from lollms.binding import LOLLMSConfig, BindingInstaller
from lollms.helpers import ASCIIColors
import yaml

class Install(BindingInstaller):
    def __init__(self, config:LOLLMSConfig=None, force_reinstall:bool=False):
        # Build parent
        super().__init__(config)
        # Get the current directory
        current_dir = Path(__file__).resolve().parent
        install_file = current_dir / ".installed"

        if not install_file.exists() or force_reinstall:
            ASCIIColors.info("-------------- llama_cpp_official binding -------------------------------")
            print("This is the first time you are using this binding.")
            # Step 2: Install dependencies using pip from requirements.txt
            requirements_file = current_dir / "requirements.txt"

            # Define the environment variables
            env = os.environ.copy()
            env["CMAKE_ARGS"] = "-DLLAMA_CUBLAS=on"
            env["FORCE_CMAKE"] = "1"
            result = subprocess.run(["pip", "install", "--upgrade", "--no-cache-dir", "-r", str(requirements_file)], env=env)

            if result.returncode != 0:
                print("Couldn't find Cuda build tools on your PC. Reverting to CPU. ")
                subprocess.run(["pip", "install", "--upgrade", "--no-cache-dir", "-r", str(requirements_file)])

            # Create ther models folder
            models_folder = config.lollms_paths.personal_models_path/f"{Path(__file__).parent.stem}"
            models_folder.mkdir(exist_ok=True, parents=True)

            # Create the configuration file
            self.create_config_file(config.lollms_paths.personal_configuration_path / 'binding_llamacpp_config.yaml')
            
            #Create the install file 
            with open(install_file,"w") as f:
                f.write("ok")
            print("Installed successfully")

    def create_config_file(self, path):
        """
        Create a local_config.yaml file with predefined data.

        The function creates a local_config.yaml file with the specified data. The file is saved in the parent directory
        of the current file.

        Args:
            None

        Returns:
            None
        """
        data = {
            "n_gpu_layers": 20,     # number of layers to put in gpu
        }
        with open(path, 'w') as file:
            yaml.dump(data, file)

