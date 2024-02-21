from typing_extensions import Any
import serff_parser as _parser
from global_config import SOURCE_FILES_DIR

def generate(parameters:dict[str, Any])->None:
    serff_parser = _parser.SERFFParser(parameters)
    serff_parser.parse_yaml_file()
    print("Generating domain files..")
    serff_parser.parse_domain()
    print("Generating repository files..")
    serff_parser.parse_repository()
    print("Generating handler files..")
    serff_parser.parse_handler()
    print("Generating test scripts..")
    ## Iteration 2
    print("Fetching SERFF source files..")
    serff_parser.fetch_source_files()
    project_directory:str = f"{serff_parser.project_name}-{serff_parser.service_name}"
    source_file_directory:str = SOURCE_FILES_DIR[serff_parser.runtime]
    serff_parser.move_source_files(source_file_directory, project_directory)
    print("Updating serverless.yml")

    print("Creating config files")

    serff_parser.generate_files()


def add_module(parameters:dict[str, Any])->None:
    serff_parser = _parser.SERFFParser(parameters)
    serff_parser.parse_yaml_file()
    print("Generating domain files..")
    serff_parser.parse_domain()
    print("Generating repository files..")
    serff_parser.parse_repository()
    print("Generating handler files..")
    serff_parser.parse_handler()
    print("Generating test scripts..")
    print("Updating serverless.yml")

def generate_global_infra(parameters:dict[str, Any])-> None:
    ## Iteration 3
    pass