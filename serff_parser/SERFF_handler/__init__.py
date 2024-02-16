from typing_extensions import Any
from serff_parser.SERFF_handler import py_handler_script
# from serff_parser.SERFF_handler import ts_handler_script
import helpers

#python directories
PY_HANDLERS_DIRECTORY:str = "app/handlers/http/"
PY_RULES_DIRECTORY:str    = "app/handlers/rules/"

#typescript directories
TS_HANDLERS_DIRECTORY:str = "app/handlers/http/"
TS_POLICIES_DIRECTORY:str = "app/handlers/_rules/policy/"
TS_SCHEMAS_DIRECTORY:str  = "app/handlers/_rules/schema/"

FUNCTION_RUNTIME_MAP:dict[str,list[Any]] = {
    "python":[
        {
            "generate_function": py_handler_script.generate_create_handler,
            "file_path": PY_HANDLERS_DIRECTORY,
            "filename_format": "create_{|module_name|}_handler"
        },
        {
            "generate_function": py_handler_script.generate_get_handler,
            "file_path": PY_HANDLERS_DIRECTORY,
            "filename_format": "get_{|module_name|}_handler"
        },
        {
            "generate_function": py_handler_script.generate_list_handler,
            "file_path": PY_HANDLERS_DIRECTORY,
            "filename_format": "list_{|module_name|}_handler"
        },
        {
            "generate_function": py_handler_script.generate_update_handler,
            "file_path": PY_HANDLERS_DIRECTORY,
            "filename_format": "update_{|module_name|}_handler"
        },
        {
            "generate_function": py_handler_script.generate_delete_handler,
            "file_path": PY_HANDLERS_DIRECTORY,
            "filename_format": "delete_{|module_name|}_handler"
        },
    ],
    "typescript":[

    ]
}

def create_handlers(module_name:str, module_attributes:dict[str, Any], runtime:str, extension:str) -> list[dict[str, str]]:
    files_to_append:list[dict[str, str]] = []
    
    for functions in FUNCTION_RUNTIME_MAP[runtime]:
        files_to_append.append({
            "file_path": helpers.compose_file_path(functions["file_path"] + f"{module_name}/", functions['filename_format'], module_name, extension),
            "source_code": functions["generate_function"](module_name, module_attributes)
        })
    return files_to_append
     
