import textwrap
from typing_extensions import Any 
import helpers

def generate_model_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    class_name: str = helpers.convert_to_system_name(module_name, "class")
    db_name: str = helpers.to_variable(module_name)
    source_code:str = f"""\
    import mongoose from "mongoose";
    import {{ getCurrentDateTime }} from "../../lib/helpers/datetime";

    const {{ Schema }} = mongoose;

    const {class_name}Schema = new Schema({{"""
    for attribute, attribute_items in module_attributes.items():
            if(attribute_items.get("data_type", "class") == 'date'):
                data_type = 'Date'
            elif(attribute_items.get("data_type", "class") == 'class'):
                data_type = 'String'
            elif(attribute_items.get("data_type", "class") == 'int'):
                data_type = 'Number'
            elif(attribute_items.get("data_type", "class") == 'number'):
                data_type = 'Number'
            elif(attribute_items.get("data_type", "class") == 'file-upload'):
                data_type = 'String'
            elif(attribute_items.get("data_type", "class") == 'string'):
                data_type = 'String'
            else:
                data_type = attribute_items.get("data_type", "class")
            

            field = helpers.to_camel_case(attribute)
            source_code += f"""
        {field}: {{
            type: {data_type}
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