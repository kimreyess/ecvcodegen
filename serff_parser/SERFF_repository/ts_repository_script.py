import textwrap
from typing_extensions import Any 
import helpers

def generate_repository_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    class_name: str = helpers.convert_to_system_name(module_name, "class")
    source_code:str = f"""\
    import ORM from "./_orm";
    import {class_name}Model from "../../models/mongodb/{class_name}Model";

    class {class_name}Repository extends ORM {{
        constructor() {{
            super({class_name}Model);
        }}
    }}

    export default {class_name}Repository;
    """

    return textwrap.dedent(source_code)