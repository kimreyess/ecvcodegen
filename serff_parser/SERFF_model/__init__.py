from typing_extensions import Any
from serff_parser.SERFF_model import py_model_script
# from serff_parser.SERFF_handler import ts_handler_script
import helpers

#python repositories
PY_MODELS_DIRECTORY = "app/models/"

#typescript directories
TS_MODELS_DIRECTORY       = "app/models/"

FUNCTION_RUNTIME_MAP:dict[str,list[Any]] = {
    "python":[
        {
            "generate_function": py_model_script.generate_model_source_code,
            "file_config":
            {
                "file_path": PY_MODELS_DIRECTORY,
                "filename_format": "{|module_name|}_model"
            }
        }
    ],
    "typescript":[

    ]
}

def create_models(module_name:str, module_attributes:dict[str, Any], runtime:str) -> list[dict[str, str]]:
    files_to_append:list[dict[str, str]] = []
    
    for functions in FUNCTION_RUNTIME_MAP[runtime]:
        files_to_append.append({
            "file_path": helpers.compose_file_path(functions["file_config"], module_name, runtime),
            "source_code": functions["generate_function"](module_name, module_attributes)
        })

    return files_to_append