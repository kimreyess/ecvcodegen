from typing_extensions import Callable
RUNTIME_EXTENSION = {
    "python": ".py",
    "typescript": ".ts"
}

def convert_to_system_name(name:str, target:str='variable')->str:

    converter_map:dict[str, Callable[..., str]] = {
        "variable":to_variable,
        "class":to_class
    }
    return converter_map[target](name)

def to_variable(temp_name:str)-> str:
    name:str = temp_name.replace(" ", "_")
    system_name = ''
    whitelist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789'

    for char in name:
        if char in whitelist:
            system_name += char
    #This also works, if rather obtuse and uses a magic method
    #system_name = ''.join(filter(whitelist.__contains__, name))

    #Must begin with letter or underscore, else prepend underscore
    if system_name[0] in '0123456789':
        system_name = '_' + system_name

    return system_name.lower()

def to_class(temp_name:str)-> str:
    name:list[str] = temp_name.split("_")
    capitalized_name = [word.capitalize() for word in name]
    return ''.join(capitalized_name)

def to_readable_name(temp_name:str)-> str:
    name:list[str] = temp_name.split("_")
    capitalized_name = [word.capitalize() for word in name]
    return ' '.join(capitalized_name)

def to_camel_case(temp_name: str) -> str:
    name = temp_name.split("_")
    capitalized_name = [name[0].lower()] + [word.capitalize() for word in name[1:]]
    return ''.join(capitalized_name)

def compose_file_path(file_config:dict[str, str], module_name:str, runtime:str)-> str:
    filename:str = ""
    if runtime == "python":
        filename = module_name
    else:
        filename = to_class(module_name)
    
    temp_file_path: str = file_config["file_path"]
    if file_config.get("sub_directories", None):
        temp_file_path = temp_file_path + replace_module_name(file_config['sub_directories'], filename)

    return temp_file_path + replace_module_name(file_config["filename_format"], filename) + RUNTIME_EXTENSION[runtime]

def replace_module_name(file_format:str, to_replace:str)->str:
    return file_format.replace("{|module_name|}", to_replace)

def get_fields(data_type:str, runtime:str)-> str:
    fields_map:dict[str, Callable[..., str]] = {
        "string": get_string_type,
        "integer": get_integer_type,
        "float": get_float_type,
        "boolean": get_boolean_type,
        "object": get_object_type,
        "array": get_array_type,
        "date": get_date_type
    }
    return fields_map[data_type](runtime)

def get_string_type(runtime:str)->str:
    str_map:dict[str, str] = {
        "python": "str",
        "typescript": "String"
    }

    return str_map[runtime]

def get_integer_type(runtime:str)->str:
    str_map:dict[str, str] = {
        "python": "int",
        "typescript": "Number"
    }

    return str_map[runtime]

def get_float_type(runtime:str)->str:
    str_map:dict[str, str] = {
        "python": "float",
        "typescript": "Number"
    }

    return str_map[runtime]

def get_boolean_type(runtime:str)->str:
    str_map:dict[str, str] = {
        "python": "bool",
        "typescript": "Boolean"
    }

    return str_map[runtime]

def get_date_type(runtime:str)->str:
    str_map:dict[str, str] = {
        "python": "string",
        # "python": "dict[Any, Any]",
        "typescript": "Date"
    }

    return str_map[runtime]

def get_object_type(runtime:str)->str:
    str_map:dict[str, str] = {
        "python": "dict[str, Any]",
        "typescript": "Object"
    }

    return str_map[runtime]

def get_array_type(runtime:str)->str:
    str_map:dict[str, str] = {
        "python": "list",
        "typescript": "Array"
    }

    return str_map[runtime]

def py_define_properties(module_attributes:dict[str, str], runtime:str) -> str:
    properties:str = """(
                        default = None,"""
    for attribute_name, attribute_value in module_attributes.items():
        if attribute_name == "required":
            if attribute_value == "false":
                properties += """
                        exclude = True,"""    
    properties += """
                    )"""

    return properties