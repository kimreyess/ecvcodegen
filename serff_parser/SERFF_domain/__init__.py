from typing_extensions import Any
from serff_parser.SERFF_domain import py_domain_script
import helpers
# from serff_parser.SERFF_domain import ts_domain_script

#python directories
PY_DOMAINS_DIRECTORY:str = "app/domains/"

#typescript directories
TS_CONTROLLERS_DIRECTORY:str = "app/controllers/"

FUNCTION_RUNTIME_MAP:dict[str,list[Any]] = {
    "python":[
        {
            "generate_function": py_domain_script.generate_domain_source_code,
            "file_config": {
                "file_path": PY_DOMAINS_DIRECTORY,
                "sub_directories": "{|module_name|}/",
                "filename_format": "{|module_name|}"
            }
        },
        {
            "generate_function": py_domain_script.generate_list_domain_source_code,
            "file_config": {
                "file_path": PY_DOMAINS_DIRECTORY,
                "sub_directories": "{|module_name|}/",
                "filename_format": "list_{|module_name|}"
            }
        },
    ],
    "typescript":[

    ]
}


def create_domain(module_name:str, module_attributes:dict[str, Any], runtime:str) -> list[dict[str, str]]:
    files_to_append:list[dict[str, str]] = []
    
    for functions in FUNCTION_RUNTIME_MAP[runtime]:
        files_to_append.append({
            "file_path": helpers.compose_file_path(functions["file_config"], module_name, runtime),
            "source_code": functions["generate_function"](module_name, module_attributes)
        })
    return files_to_append
    
