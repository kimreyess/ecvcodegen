from typing_extensions import Any

import subprocess
import platform
import os

def update(parameters: dict[str, Any]) -> None:
    subprocess.run(['mason', 'upgrade', '--global'], check=True)
    

def generate(parameters:dict[str, Any])->None:
    template = parameters['template']
    path = []
    config = []
    if parameters.get('path'):
        path = ['-o', parameters['path']]

    if parameters.get('config'):
        config = ['-c', parameters['config']]
    
    command = ['mason', 'make', template] + path + config
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running 'mason make {template}': {e}")

# def init(parameters: dict[str, Any]) -> None:
#     os_type: str = platform.system()
#     remove_mason_file()
    
#     if os_type == 'Windows':
#         print('This package is not supported on Windows Operating System. Use WSL instead.')
#     else:
#         download_command = ["curl", "-fsSL", "https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"]
#         install_command = ["/bin/bash"]
#         download_process = subprocess.run(download_command, capture_output=True, text=True)

#         if download_process.returncode == 0:
#             install_process = subprocess.run(install_command, input=download_process.stdout, text=True)
#             if install_process.returncode == 0:
#                 brew = subprocess.run(['which', 'brew'], capture_output=True, text=True)
#                 brew_path = brew.stdout.strip()
#                 add_brew_to_all_shells(brew_path)
#                 print("Homebrew installed successfully.")

#                 result = subprocess.run([brew_path, 'tap', 'felangel/mason'], check=True)

#                 if result.returncode == 0:
#                     subprocess.run([brew_path, 'install', 'mason'], check=True)
#                     print("mason-cli downloaded successfully!")
#                     mason = subprocess.run(['which', 'mason'], capture_output=True, text=True)
#                     mason_path = mason.stdout.strip()
#                     subprocess.run([mason_path, 'cache', 'clear'], check=True)
#                     subprocess.run([mason_path, 'init'], check=True)
#                     subprocess.run([mason_path, 'add', '-g', 'flutter_model', '--git-url', 'https://Arlovzki@bitbucket.org/arlovzki/ecv_flutter_mason_bricks.git', '--git-path', 'flutter_model'], check=True)
#                     subprocess.run([mason_path, 'add', '-g', 'flutter_boilerplate', '--git-url', 'https://Arlovzki@bitbucket.org/arlovzki/ecv_flutter_mason_bricks.git', '--git-path', 'flutter_boilerplate'], check=True)  
#                 else:
#                     print("Failed to download mason-cli.")
#             else:
#                 print("Failed to install Homebrew.")
#         else:
#             print("Failed to download Homebrew installation script.")

def init(parameters: dict[str, Any]) -> None:
    add_path_to_all_shells()
    os_type: str = platform.system()
    remove_mason_file()

    if os_type == 'Windows':
        print('This package is not supported on Windows Operating System. Use WSL instead.')
    else:
        subprocess.run(['dart', '--disable-analytics'], check=True)
        result = subprocess.run(['dart', 'pub', 'global', 'activate', 'mason_cli'], check=True)

        if result.returncode == 0:
            print("mason-cli downloaded successfully!")
            subprocess.run(['mason', 'cache', 'clear'], check=True)
            subprocess.run(['mason', 'init'], check=True)
            subprocess.run(['mason', 'add', '-g', 'flutter_model', '--git-url', 'https://Arlovzki@bitbucket.org/arlovzki/ecv_flutter_mason_bricks.git', '--git-path', 'flutter_model'], check=True)
            subprocess.run(['mason', 'add', '-g', 'flutter_boilerplate', '--git-url', 'https://Arlovzki@bitbucket.org/arlovzki/ecv_flutter_mason_bricks.git', '--git-path', 'flutter_boilerplate'], check=True)  
        else:
            print("Failed to download mason-cli.")

def remove_mason_file():
    current_directory = os.getcwd()
    mason_yaml_path = os.path.join(current_directory, "mason.yaml")
    
    if os.path.exists(mason_yaml_path):
        os.remove(mason_yaml_path)


def add_path_to_shell_rc(rc_file_path:str):
    with open(rc_file_path, "r") as rc_file:
        rc_content = rc_file.read()
        if f'export PATH="$PATH":"$HOME/.pub-cache/bin"' not in rc_content:
            with open(rc_file_path, "a") as rc:
                rc.write(f'\n# Adding path\nexport PATH="$PATH":"$HOME/.pub-cache/bin"\n')
                rc.write(f'export PATH="$PATH:/usr/lib/dart/bin"\n')
            print(f"Added path to {rc_file_path}")
        else:
            print(f"Path already exists in {rc_file_path}. Skipping.")

def add_path_to_all_shells():
    home_directory = os.path.expanduser("~")
    shell_rc_files = [".bashrc", ".zshrc", ".profile"]  # Add other shell config files as needed
    
    for rc_file in shell_rc_files:
        rc_file_path = os.path.join(home_directory, rc_file)
        if os.path.exists(rc_file_path):
            add_path_to_shell_rc(rc_file_path)
        else:
            print(f"{rc_file_path} does not exist. Skipping.")