import yaml
import boto3
from typing_extensions import Any
import serff_parser.SERFF_domain as domain_parser
import serff_parser.SERFF_handler as handler_parser
import serff_parser.SERFF_repository as repository_parser
# import serff_parser.SERFF_test_scripts as test_script_parser
import helpers
import os
import subprocess
import shutil

class SERFFParser():

    FILE_PATH_MAP = {
        "domain": "app/domains/",
        "repository": "app/repositories/",
        "handler": "app/handlers/http/",
        "exception": "app/exceptions/"
    }

    RUNTIME_REPOSITORY_CONFIG:"dict[str,dict[str,str]]" = {
        "python": {
            "repository_name": "ecv-python-serverless-framework",
            "temp_dir": "source_files/py-serff/"

        }
    }


    def __init__(self, params:dict[str, str]):
        self._raw = None
        self._model:dict[str, dict[str,Any]] = {}
        self._files:list[dict[str, Any]] = []
        self.project_name = params["project"]
        self.service_name = params["service"]
        self.runtime = params["runtime"]


        if params["file"]:
            with open(params["file"]) as f:
                self._raw = yaml.safe_load(f.read())
    
    def parse_yaml_file(self) -> None:
        # parse yaml file here..
        # YAML file structure:
        #__SERFF_settings__ contains project configuration setting you want to specify, 
        #                   for example what database engine and database/table/cluster name to use 
        #__Modules__ contains the information to be extracted and parsed for your microservice
        temp_dict:dict[str, Any] = {}

        for module, module_items in self._raw["__Modules__"].items(): #type: ignore
            temp_columns:dict[str,Any] = {}
            for column_name, column_attributes in module_items["data"].items(): #type: ignore
                if isinstance(column_attributes, str):
                    temp_column_attributes = {
                        "data_type": column_attributes
                        }
                else:
                    temp_column_attributes:dict[str, Any] = column_attributes #type: ignore
                temp_columns.update({
                            helpers.convert_to_system_name(column_name):temp_column_attributes # type: ignore
                        })

            temp_dict.update({
                helpers.convert_to_system_name(module):temp_columns # type: ignore
                })

        self._model = temp_dict            
    
    def parse_domain(self) -> None:
        temp_files:list[dict[str, Any]] = []
        for module, attributes in self._model.items():
            temp_files = temp_files + domain_parser.create_domain(module, attributes, self.runtime)
        self._files = self._files + temp_files    
        pass

    def parse_handler(self) -> None:
        temp_files:list[dict[str, Any]] = []
        for module, attributes in self._model.items():
            temp_files = temp_files + handler_parser.create_handlers(module, attributes, self.runtime)
        self._files = self._files + temp_files
        pass

    def parse_repository(self) -> None:
        temp_files:list[dict[str, Any]] = []
        for module, attributes in self._model.items():
            temp_files = temp_files + repository_parser.create_repositories(module, attributes, self.runtime)
        self._files = self._files + temp_files
        pass

    def parse_test_scripts(self) -> None:
        # domain_parser code here..
        pass

        
    def generate_files(self) -> None:
        cwd:str = os.getcwd()
        for items in self._files:
            filename: str = f"{self.project_name}-{self.service_name}/{items['file_path']}"
            directory: str = os.path.dirname(cwd+"/"+filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            content:str = items["source_code"]
            with open(filename, "w") as file:
                file.write(content)

    def fetch_source_files(self):
        codecommit: Any = boto3.client('codecommit') #type: ignore
        if os.path.exists(self.RUNTIME_REPOSITORY_CONFIG[self.runtime]['temp_dir']):
            print("Source file already exist, checking for updates..")
            ## pull to make sure serff version is upto date
            try:
                subprocess.run(["git", "pull"], cwd=self.RUNTIME_REPOSITORY_CONFIG[self.runtime]['temp_dir'], check=True)
                print("Pull operation completed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
                print("Pull operation failed.")
        else:
            try:
                response = codecommit.get_repository(repositoryName=self.RUNTIME_REPOSITORY_CONFIG[self.runtime]["repository_name"])
                repository:dict[str, Any] = response["repositoryMetadata"]

                # Clone the repository
                clone_url = repository['cloneUrlSsh']  # Use HTTPS clone URL for cloning
                clone_command = f"git clone {clone_url} {self.RUNTIME_REPOSITORY_CONFIG[self.runtime]['temp_dir']}"
                subprocess.check_output(clone_command, shell=True) #type: ignore

                print(f"Repository '{self.RUNTIME_REPOSITORY_CONFIG[self.runtime]['repository_name']}' cloned successfully'.")
            except codecommit.exceptions.RepositoryDoesNotExistException:
                print(f"Error: Repository '{self.RUNTIME_REPOSITORY_CONFIG[self.runtime]['repository_name']}' does not exist.")
            except Exception as e:
                print(f"Error: {e}")            
        
    @staticmethod
    def move_source_files(source_dir:str, destination_dir:str):
            """
            Copy the contents of a directory to another directory.
            
            Args:
            source_dir (str): The source directory.
            destination_dir (str): The destination directory.
            
            Returns:
            None
            """

            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            
            for item in os.listdir(source_dir):
                source_item = os.path.join(source_dir, item)
                destination_item = os.path.join(destination_dir, item)
                ## do not include .git
                if item not in [".git"] and not item.startswith(f'{source_dir}\.git'):#type: ignore
                    if os.path.isdir(source_item):
                        shutil.copytree(source_item, destination_item, symlinks=True)
                    else:
                        shutil.copy2(source_item, destination_item)

    

        


