from typing_extensions import Any
from serff_parser.SERFF_handler import py_handler_script
from serff_parser.SERFF_handler import ts_handler_script
from serff_parser.SERFF_handler import ts_handler_policies
from serff_parser.SERFF_handler import ts_handler_schema
import helpers

#python directories
PY_HANDLERS_DIRECTORY:str = "app/handlers/http/"
PY_RULES_DIRECTORY:str    = "app/handlers/rules/"

#typescript directories
TS_HANDLERS_DIRECTORY:str = "app/handlers/http/"
TS_POLICIES_DIRECTORY:str = "app/handlers/http/_rules/policies/"
TS_SCHEMAS_DIRECTORY:str  = "app/handlers/http/_rules/schemas/"

FUNCTION_RUNTIME_MAP:dict[str,list[Any]] = {
    "python":[
        {
            "generate_function": py_handler_script.generate_create_handler,
            "file_config":{
                "file_path": PY_HANDLERS_DIRECTORY,
                "filename_format": "create_{|module_name|}_handler",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": py_handler_script.generate_get_handler,
            "file_config":{
                "file_path": PY_HANDLERS_DIRECTORY,
                "filename_format": "get_{|module_name|}_handler",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": py_handler_script.generate_list_handler,
            "file_config":{
                "file_path": PY_HANDLERS_DIRECTORY,
                "filename_format": "list_{|module_name|}_handler",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": py_handler_script.generate_update_handler,
            "file_config":{
                "file_path": PY_HANDLERS_DIRECTORY,
                "filename_format": "update_{|module_name|}_handler",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": py_handler_script.generate_delete_handler,
            "file_config":{
                "file_path": PY_HANDLERS_DIRECTORY,
                "filename_format": "delete_{|module_name|}_handler",
                "sub_directories": "{|module_name|}/"
            }
        },
    ],
    "typescript":[
        {
            "generate_function": ts_handler_policies.generate_rule_policies_handler,
            "file_config":{
                "file_path": TS_POLICIES_DIRECTORY,
                "filename_format": "{|module_name|}",
            }
        },
        {
            "generate_function": ts_handler_schema.generate_create_rule_schema_code,
            "file_config":{
                "file_path": TS_SCHEMAS_DIRECTORY,
                "filename_format": "create",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_schema.generate_get_rule_schema_code,
            "file_config":{
                "file_path": TS_SCHEMAS_DIRECTORY,
                "filename_format": "get",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_schema.generate_delete_rule_schema_code,
            "file_config":{
                "file_path": TS_SCHEMAS_DIRECTORY,
                "filename_format": "delete",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_schema.generate_update_rule_schema_code,
            "file_config":{
                "file_path": TS_SCHEMAS_DIRECTORY,
                "filename_format": "update",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_schema.generate_list_rule_schema_code,
            "file_config":{
                "file_path": TS_SCHEMAS_DIRECTORY,
                "filename_format": "list",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_schema.generate_search_rule_schema_code,
            "file_config":{
                "file_path": TS_SCHEMAS_DIRECTORY,
                "filename_format": "search",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_script.generate_create_handler,
            "file_config":{
                "file_path": TS_HANDLERS_DIRECTORY,
                "filename_format": "create",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_script.generate_get_handler,
            "file_config":{
                "file_path": TS_HANDLERS_DIRECTORY,
                "filename_format": "get",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_script.generate_list_handler,
            "file_config":{
                "file_path": TS_HANDLERS_DIRECTORY,
                "filename_format": "list",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_script.generate_update_handler,
            "file_config":{
                "file_path": TS_HANDLERS_DIRECTORY,
                "filename_format": "update",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_script.generate_delete_handler,
            "file_config":{
                "file_path": TS_HANDLERS_DIRECTORY,
                "filename_format": "delete",
                "sub_directories": "{|module_name|}/"
            }
        },
        {
            "generate_function": ts_handler_script.generate_search_handler,
            "file_config":{
                "file_path": TS_HANDLERS_DIRECTORY,
                "filename_format": "search",
                "sub_directories": "{|module_name|}/"
            }
        }
    ]
}

def create_handlers(module_name:str, module_attributes:dict[str, Any], runtime:str) -> list[dict[str, str]]:
    files_to_append:list[dict[str, str]] = []
    
    for functions in FUNCTION_RUNTIME_MAP[runtime]:
        files_to_append.append({
            "file_path": helpers.compose_file_path(functions["file_config"], module_name, runtime),
            "source_code": functions["generate_function"](module_name, module_attributes)
        })
    return files_to_append
     
