from __future__ import annotations
import helpers
import textwrap
from typing_extensions import Any
RUNTIME = "typescript"


def generate_create_rule_schema_code(module_name:str, module_attributes:dict[str, Any]):
    # class_name = helpers.to_class(module_name)
    # class_name_lowercase = helpers.to_camel_case(module_name)
    
    source_code = f"""
    import Joi from "joi";

    // Schema
    export default Joi.object({{"""
    for attribute, attribute_items in module_attributes.items():
        field = helpers.to_camel_case(attribute)
        source_code += f"""
        {field}: Joi.{(helpers.get_fields(attribute_items.get('data_type', 'string'), RUNTIME).lower())}().required(),"""

    source_code += f"""
    }})"""

    return textwrap.dedent(source_code)


def generate_update_rule_schema_code(module_name:str, module_attributes:dict[str, Any]):
    # class_name = helpers.to_class(module_name)
    # class_name_lowercase = helpers.to_camel_case(module_name)
    
    source_code = f"""
    import Joi from "joi";

    // Schema
    export default Joi.object({{
        id: Joi.string().required(),"""
    for attribute, attribute_items in module_attributes.items():
        field = helpers.to_camel_case(attribute)
        source_code += f"""
        {field}: Joi.{(helpers.get_fields(attribute_items.get('data_type', 'string'), RUNTIME).lower())}(),"""

    source_code += f"""
    }})"""

    return textwrap.dedent(source_code)

def generate_get_rule_schema_code(module_name:str, module_attributes:dict[str, Any]):
    # class_name = helpers.to_class(module_name)
    # class_name_lowercase = helpers.to_camel_case(module_name)
    
    source_code = f"""
    import Joi from "joi";

    // Schema
    export default Joi.object({{
        id: Joi.string().required(),
    }});"""
    

    return textwrap.dedent(source_code)

def generate_delete_rule_schema_code(module_name:str, module_attributes:dict[str, Any]):
    # class_name = helpers.to_class(module_name)
    # class_name_lowercase = helpers.to_camel_case(module_name)
    
    source_code = f"""
    import Joi from "joi";

    // Schema
    export default Joi.object({{
        id: Joi.string().required(),
    }});"""
    

    return textwrap.dedent(source_code)


def generate_list_rule_schema_code(module_name:str, module_attributes:dict[str, Any]):
    # class_name = helpers.to_class(module_name)
    # class_name_lowercase = helpers.to_camel_case(module_name)
    
    source_code = f"""
    import Joi from "joi";

    // Schema
    export default Joi.object({{
        page: Joi.number().min(1).required(),
        pageSize: Joi.number().min(10).required(),
        returnCount: Joi.boolean().required(),
        likeFilters: Joi.array().items(
            Joi.object({{
                keys: Joi.array().items(Joi.string().required()).required(),
                value: Joi.string().required(),
            }})
        ),
        equalFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.string().allow(null).required(),
            }})
        ),
        notEqualFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.any().allow(null).required(),
            }})
        ),
        inFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.array().items(Joi.string().required()).required(),
            }})
        ),
        notInFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.array().items(Joi.string().required()).required(),
            }})
        ),
        betweenFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.array().items(Joi.string().required()).length(2).required(),
            }})
        ),
        sorts: Joi.array().items(Joi.string().regex(/^[a-zA-Z_]+:(asc|desc)$/)),
    }});
    """
    
    return textwrap.dedent(source_code)


def generate_search_rule_schema_code(module_name:str, module_attributes:dict[str, Any]):
    # class_name = helpers.to_class(module_name)
    # class_name_lowercase = helpers.to_camel_case(module_name)
    
    source_code = f"""
    import Joi from "joi";

    // Schema
    export default Joi.object({{
        limit: Joi.number().min(10).required(),
        likeFilters: Joi.array().items(
            Joi.object({{
                keys: Joi.array().items(Joi.string().required()).required(),
                value: Joi.string().required(),
            }})
        ),
        equalFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.string().allow(null).required(),
            }})
        ),
        notEqualFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.any().allow(null).required(),
            }})
        ),
        inFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.array().items(Joi.string().required()).required(),
            }})
        ),
        notInFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.array().items(Joi.string().required()).required(),
            }})
        ),
        betweenFilters: Joi.array().items(
            Joi.object({{
                key: Joi.string().required(),
                value: Joi.array().items(Joi.string().required()).length(2).required(),
            }})
        ),
        sorts: Joi.array().items(Joi.string().regex(/^[a-zA-Z_]+:(asc|desc)$/)),
    }});
    """
    
    return textwrap.dedent(source_code)