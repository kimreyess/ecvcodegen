from typing_extensions import Any
from serff_parser.SERFF_repository import py_repository_script
from serff_parser.SERFF_repository import ts_repository_script
from serff_parser.SERFF_repository import ts_model_script
import helpers

#python repositories
PY_REPOSITORIES_DIRECTORY = "app/services/repositories/"

#typescript directories
TS_REPOSITORIES_DIRECTORY = "app/repositories/mongodb/"
TS_MODELS_DIRECTORY       = "app/models/mongodb/"

FUNCTION_RUNTIME_MAP:dict[str,list[Any]] = {
    "python":[
        {
            "generate_function": py_repository_script.generate_repository_source_code,
            "file_config":
            {
                "file_path": PY_REPOSITORIES_DIRECTORY,
                "filename_format": "{|module_name|}_repository"
            }
        }
    ],
    "typescript":[
        {
            "generate_function": ts_repository_script.generate_repository_source_code,
            "file_path": TS_REPOSITORIES_DIRECTORY,
            "filename_format": "{|module_name|}Repository"
        },
        {
            "generate_function": ts_model_script.generate_model_source_code,
            "file_path": TS_MODELS_DIRECTORY,
            "filename_format": "{|module_name|}Model"
        }
    ]
}

def create_repositories(module_name:str, module_attributes:dict[str, Any], runtime:str) -> list[dict[str, str]]:
    files_to_append:list[dict[str, str]] = []
    
    for functions in FUNCTION_RUNTIME_MAP[runtime]:
        files_to_append.append({
            "file_path": helpers.compose_file_path(functions["file_config"], module_name, runtime),
            "source_code": functions["generate_function"](module_name, module_attributes)
        })

    return files_to_append