from typing_extensions import Any, Callable
from serff_parser.SERFF_handler import py_handler_script
# from serff_parser.SERFF_handler import ts_handler_script

import helpers

FUNCTION_RUNTIME_MAP = {
    "python": py_handler_script,
}

def create_handlers(module_name:str, module_attributes:dict[str, Any], runtime:str, file_path:str, extension:str) -> list[dict[str, str]]:
    files_to_append:list[dict[str, str]] = []
    
    default_handlers:dict[str, Callable[..., str]] = {
        "create": FUNCTION_RUNTIME_MAP[runtime].generate_create_handler, 
        "get": FUNCTION_RUNTIME_MAP[runtime].generate_get_handler,  
        "list": FUNCTION_RUNTIME_MAP[runtime].generate_list_handler, 
        "update": FUNCTION_RUNTIME_MAP[runtime].generate_update_handler, 
        "delete": FUNCTION_RUNTIME_MAP[runtime].generate_delete_handler, 
    }
    
    for handler, functions in default_handlers.items():
        files_to_append.append({
            "file_path": helpers.compose_file_path(file_path + f"{module_name}/", f"{handler}_{module_name}_handler", extension),
            "source_code": functions(module_name, module_attributes)
        })
    return files_to_append
     
