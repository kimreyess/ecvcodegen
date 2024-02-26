import textwrap
from typing_extensions import Any 
import helpers
RUNTIME = "typescript"
def generate_model_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    class_name: str = helpers.convert_to_system_name(module_name, "class")
    db_name: str = helpers.to_variable(module_name)
    source_code:str = f"""\
    import mongoose from "mongoose";
    import {{ getCurrentDateTime }} from "../../lib/helpers/datetime";

    const {{ Schema }} = mongoose;

    const {class_name}Schema = new Schema({{"""
    for attribute, attribute_items in module_attributes.items():
        field = helpers.to_camel_case(attribute)
        source_code += f"""
        {field}: {{
            type: {helpers.get_fields(attribute_items.get('data_type', 'object'), RUNTIME)}
        }},"""   
    source_code += f"""
        logs: Array,
        createdAt: {{
            type: Date,
            default: getCurrentDateTime(),
        }},
        createdBy: {{
            type: String,
            default: null,
        }},
        createdByCognitoId: {{
            type: String,
            default: null,
        }},
        updatedAt: {{
            type: Date,
            default: null,
        }},
        updatedBy: {{
            type: String,
            default: null,
        }},
        updatedByCognitoId: {{
            type: String,
            default: null,
        }},
    }});

    const model = mongoose.model("{class_name}", {class_name}Schema, "{db_name}");
    model.syncIndexes();

    export default model;

    """

    return textwrap.dedent(source_code)