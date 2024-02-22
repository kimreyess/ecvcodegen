import textwrap
from typing_extensions import Any 
import helpers
RUNTIME = "python"

def generate_model_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    class_name: str = helpers.convert_to_system_name(module_name, "class")

    model_source_code: str = ""
    response_source_code: str = ""

    for attribute, attribute_property in module_attributes.items():
        model_source_code += f"{attribute}: {helpers.get_fields(attribute_property.get('data_type', 'object'), RUNTIME)} = field"
        model_source_code += f"""{helpers.py_define_properties(attribute_property, RUNTIME)}
        """

        response_source_code += f"""
        '{attribute}',"""

    source_code:str = f"""\
    from __future__ import annotations
    from typing_extensions import Any
    from ecv_python_development.database.pydantic import BaseModel, field

    class {class_name}Model(BaseModel):
        {model_source_code}
    
    CREATE_RESPONSE = {{{response_source_code}
    }}

    """

    return textwrap.dedent(source_code)