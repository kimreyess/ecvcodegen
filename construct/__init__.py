from typing_extensions import Any
import serff_parser as _parser
from global_config import SOURCE_FILES_DIR

def generate(parameters:dict[str, Any])->None:
    
    serff_parser              = _parser.SERFFParser(parameters)
    project_directory:str     = f"{serff_parser.project_name}-{serff_parser.service_name}"
    source_file_directory:str = SOURCE_FILES_DIR[serff_parser.runtime]
    iac_path:str              = f"{project_directory}/serverless.yml"

    print("Scanning YAML file..")
    serff_parser.parse_yaml_file()
    print("Generating domain files..")
    serff_parser.parse_domain()
    print("Generating repository files..")
    serff_parser.parse_repository()
    print("Generating handler files..")
    serff_parser.parse_handler()
    print("Generating model files..")
    serff_parser.parse_model()
    # print("Generating test scripts..")
    ## Iteration 2
    print("Fetching SERFF source files..")
    serff_parser.fetch_source_files()
    serff_parser.move_source_files(source_file_directory, project_directory)
    print("Updating serverless.yml")
    serff_parser.parse_iac_template(iac_path)
    print("Creating config files")

    serff_parser.generate_files()
    print(f"{project_directory} successfully created.")


def add_module(parameters:dict[str, Any])->None:

    serff_parser              = _parser.SERFFParser(parameters)
    project_directory:str     = f"{serff_parser.project_name}-{serff_parser.service_name}"
    iac_path:str              = f"{project_directory}/serverless.yml"

    print("Scanning YAML file..")
    serff_parser.parse_yaml_file()
    print("Generating domain files..")
    serff_parser.parse_domain()
    print("Generating repository files..")
    serff_parser.parse_repository()
    print("Generating handler files..")
    serff_parser.parse_handler()
    print("Generating model files..")
    serff_parser.parse_model()
    # print("Generating test scripts..")
    print("Updating serverless.yml")
    serff_parser.parse_iac_template(iac_path)
    
    serff_parser.generate_files()
    
    print(f"New modules successfully created.")

def generate_global_infra(parameters:dict[str, Any])-> None:
    ## Iteration 3
    pass

def run_init():
    ## create a source_files directory in home directory of your terminal
    ## check if serff is existing in your aws account, need to make sure that the current access keys is from ECV POC
    pass