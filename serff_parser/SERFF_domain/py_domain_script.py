import helpers
import textwrap
from typing_extensions import Any

def generate_domain_source_code(module_name:str, module_attributes:dict[str, Any]) -> str:
    source_code: str = f"""\
    from app.domains.base_domain import BaseDomain

    class {helpers.convert_to_system_name(module_name, "class")}(BaseDomain):
    
        METADATA = {{"""
    for attribute, attribute_items in module_attributes.items():

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
        }}

        def __init__(self, repository, data):
            self.data = data
            self.repository = repository
            self.deserialize()

    """

    return textwrap.dedent(source_code)

def generate_list_domain_source_code(module_name:str, module_attributes:dict[str, Any]):
    source_code = f"""\
    from app.domains.base_domain import BaseDomain
    from app.domains.list_base_domain import ListBaseDomain

    class {helpers.convert_to_system_name(module_name, "class")}List(ListBaseDomain):
        DOMAIN_OBJECT = {helpers.convert_to_system_name(module_name, "class")}
        DOMAIN_NAME   = "{module_name}"
    """

    return textwrap.dedent(source_code)