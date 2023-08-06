import subprocess
from pathlib import Path
import requests
from tqdm import tqdm
import yaml
from lollms.paths import LollmsPaths
from lollms.personality import AIPersonality, AIPersonalityInstaller

class Install(AIPersonalityInstaller):
    def __init__(self, personality:AIPersonality, force_reinstall=False):
        super().__init__(personality)
        root_dir = personality.lollms_paths.personal_models_path
        current_dir = Path(__file__).resolve().parent.parent

        # We put this in the shared folder in order as this can be used by other personalities.
        shared_folder = root_dir/"shared"
        sd_folder = shared_folder / "sd"
        install_file = current_dir / ".installed"

        if not sd_folder.exists():
            print("-------------- GPT4ALL backend -------------------------------")
            print("This is the first time you are using this backend.")
            print("Installing ...")
            try:
                print("Checking pytorch")
                import torch
                import torchvision
                if torch.cuda.is_available():
                    print("CUDA is supported.")
                else:
                    print("CUDA is not supported. Reinstalling PyTorch with CUDA support.")
                    self.reinstall_pytorch_with_cuda()
            except Exception as ex:
                self.reinstall_pytorch_with_cuda()

            # Step 1: Clone repository
            subprocess.run(["git", "clone", "https://github.com/CompVis/stable-diffusion.git", str(sd_folder)])

            # Step 5: Install the Python package inside sd folder
            subprocess.run(["pip", "install", "--upgrade", str(sd_folder)])

            # Step 3: Create models/Stable-diffusion folder if it doesn't exist
            models_folder = shared_folder / "sd_models"
            models_folder.mkdir(parents=True, exist_ok=True)

            # Step 4: Download model file
            model_url = "https://huggingface.co/Lykon/DreamShaper/resolve/main/DreamShaper_5_beta2_noVae_half_pruned.ckpt"
            model_file = models_folder / "DreamShaper_5_beta2_noVae_half_pruned.ckpt"
            
            # Download with progress using tqdm
            response = requests.get(model_url, stream=True)
            total_size = int(response.headers.get("content-length", 0))
            block_size = 1024  # 1KB
            progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)

            # Create configuration file
            self.create_config_file()
            
            with open(model_file, "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            
            progress_bar.close()
            
    def reinstall_pytorch_with_cuda(self):
        subprocess.run(["pip", "install", "--upgrade", "torch", "torchvision", "torchaudio", "--no-cache-dir", "--index-url", "https://download.pytorch.org/whl/cu117"])

    def create_config_file(self):
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
            "model_name": "DreamShaper_5_beta2_noVae_half_pruned.ckpt",     # good
            "max_generation_prompt_size": 512,                              # maximum number of tokens per generation prompt
            "num_images": 1,                                                # Number of images to build
            "seed": -1                                                      # seed
        }
        path = self.personality.lollms_paths.personal_configuration_path / 'personality_ascii_artist_config.yaml'
        with open(path, 'w') as file:
            yaml.dump(data, file)