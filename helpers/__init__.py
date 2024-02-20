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