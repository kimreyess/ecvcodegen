from typing_extensions import Callable
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

def compose_file_path(file_path:str, filename:str, extension:str)-> str:
    return file_path + filename + extension