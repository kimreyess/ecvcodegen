from typing_extensions import Any
from serff_parser.SERFF_iac import py_iac_script
from serff_parser.SERFF_iac import ts_iac_script
# from serff_parser.SERFF_handler import ts_handler_script

#python repositories
PY_REPOSITORIES_DIRECTORY = "app/models/"

#typescript directories
TS_MODELS_DIRECTORY       = "app/models/mongodb/"

FUNCTION_RUNTIME_MAP:dict[str,list[Any]] = {
    "python":[
        {
            "generate_function": py_iac_script.generate_lambda_create_handler_iac_source_code,
        },
        {
            "generate_function": py_iac_script.generate_lambda_list_handler_iac_source_code,
        },
        {
            "generate_function": py_iac_script.generate_lambda_update_handler_iac_source_code,
        },
        {
            "generate_function": py_iac_script.generate_lambda_get_handler_iac_source_code,
        },
        {
            "generate_function": py_iac_script.generate_lambda_delete_handler_iac_source_code,
        }
    ],
    "typescript":[
        {
            "generate_function": ts_iac_script.generate_lambda_create_handler_iac_source_code,
        },
        {
            "generate_function": ts_iac_script.generate_lambda_list_handler_iac_source_code,
        },
        {
            "generate_function": ts_iac_script.generate_lambda_update_handler_iac_source_code,
        },
        {
            "generate_function": ts_iac_script.generate_lambda_get_handler_iac_source_code,
        },
        {
            "generate_function": ts_iac_script.generate_lambda_delete_handler_iac_source_code,
        },
        {
            "generate_function": ts_iac_script.generate_lambda_search_handler_iac_source_code,
        }
    ]
}

def compose_iac_function_template(module_name:str, module_attributes:dict[str, Any], runtime:str) -> list[str]:
    iac_source_code: list[str]= []
    
    for functions in FUNCTION_RUNTIME_MAP[runtime]:
        iac_source_code.append(functions["generate_function"](module_name, module_attributes))

    return iac_source_code