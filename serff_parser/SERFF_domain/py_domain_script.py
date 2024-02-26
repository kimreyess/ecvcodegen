import helpers
import textwrap
from typing_extensions import Any

def generate_domain_source_code(module_name:str, module_attributes:dict[str, Any]) -> str:
    source_code: str = f"""\
    from typing_extensions import Any
    from app.domains.base_domain import BaseDomain

    class {helpers.convert_to_system_name(module_name, "class")}(BaseDomain):
    
        METADATA:dict[str, dict[str,Any]] = {{"""
    allowed_sort_fields:list[str] = []
    for attribute, attribute_items in module_attributes.items():
        allowed_sort_fields.append(f"'{attribute}'")
        data_type = attribute_items.get("data_type", "class")
        allowed = attribute_items.get("allowed", None)
        allowed_src_code = f"'allowed':{allowed}" if allowed else ""
        source_code += f"""
            '{attribute}': {{
                'type': '{data_type}',              
                'value': '',
                'required': True,
                'empty': False,
                'max_length': '',
                {allowed_src_code}
            }},"""  
    source_code += f"""
            "search_val":{{
                "type": "string",
                "required": False,
                "empty": False,
                "is_transient": True
            }},
            "sort_order":{{
                "type": "string",
                "required": False,
                "empty": False,
                "is_transient": True,
                "allowed": [
                    "ASCENDING",
                    "DESCENDING",
                ]
            }},
            "sort_field":{{
                "type": "string",
                "required": False,
                "empty": False,
                "is_transient": True,
                "allowed": [{', '.join(allowed_sort_fields)}]
            }}
        }}

        def __init__(self, repository, data):  #type: ignore
            self.data = data
            self.repository = repository
            self.deserialize(data)  #type: ignore

    """

    return textwrap.dedent(source_code)

def generate_list_domain_source_code(module_name:str, module_attributes:dict[str, Any]):
    class_name:str = helpers.convert_to_system_name(module_name, "class")
    source_code = f"""\
    from app.domains.list_base_domain import ListBaseDomain
    from app.domains.{module_name}.{module_name} import {class_name}

    class {class_name}List(ListBaseDomain):
        DOMAIN_OBJECT = {class_name}
        DOMAIN_NAME   = "{module_name}"
    """

    return textwrap.dedent(source_code)