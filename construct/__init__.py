from typing_extensions import Any
import serff_parser as _parser

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
    print("Fetching SERFF source files..")

    print("Updating serverless.yml")

    print("Creating config files")

    serff_parser.generate_files()


def add_module(parameters:dict[str, Any])->None:
    print("Generating domain files..")
    print("Generating repository files..")
    print("Generating handler files..")
    print("Generating test scripts..")
    print("Updating serverless.yml")
