from typing_extensions import Any
from serff_parser.SERFF_domain import py_domain_script
# from serff_parser.SERFF_domain import ts_domain_script

FUNCTION_RUNTIME_MAP = {
    "python": py_domain_script,
}

def create_domain(module_name:str, module_attributes:dict[str, Any], runtime:str) -> str:
    return FUNCTION_RUNTIME_MAP[runtime].generate_domain_source_code(module_name, module_attributes)
    
