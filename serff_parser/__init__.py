import yaml
from typing_extensions import Any
import serff_parser.SERFF_domain as domain_parser
import serff_parser.SERFF_handler as handler_parser
import serff_parser.SERFF_repository as repository_parser
# import serff_parser.SERFF_test_scripts as test_script_parser
import helpers
import os
class SERFFParser():

    FILE_PATH_MAP = {
        "domain": "app/domains/",
        "repository": "app/repositories/",
        "handler": "app/handlers/http/",
        "exception": "app/exceptions/"
    }


    def __init__(self, params:dict[str, str]):
        self._raw = None
        self._model:dict[str, dict[str,Any]] = {}
        self._files:list[dict[str, Any]] = []
        self._project_name = params["project"]
        self._service_name = params["service"]
        self._runtime = params["runtime"]


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
            temp_files = temp_files + domain_parser.create_domain(module, attributes, self._runtime)
        self._files = self._files + temp_files    
        pass

    def parse_handler(self) -> None:
        temp_files:list[dict[str, Any]] = []
        for module, attributes in self._model.items():
            temp_files = temp_files + handler_parser.create_handlers(module, attributes, self._runtime)
        self._files = self._files + temp_files
        pass

    def parse_repository(self) -> None:
        temp_files:list[dict[str, Any]] = []
        for module, attributes in self._model.items():
            temp_files = temp_files + repository_parser.create_repositories(module, attributes, self._runtime)
        self._files = self._files + temp_files
        pass

    def parse_test_scripts(self) -> None:
        # domain_parser code here..
        pass

        
    def generate_files(self) -> None:
        cwd:str = os.getcwd()
        for items in self._files:
            filename: str = f"{self._project_name}-{self._service_name}/{items['file_path']}"
            directory: str = os.path.dirname(cwd+"/"+filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            content:str = items["source_code"]
            with open(filename, "w") as file:
                file.write(content)

