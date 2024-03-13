from typing_extensions import Optional,Sequence, Any
import argparse
import os
import exceptions as _exceptions


# VALIDATION CLASSES

class ValidateGenerateCommand(argparse.Action):
    def __call__(self, parser: Any, args: Any, values: str | Sequence[Any], option_string: Optional[str|None]=None) -> None: # type: ignore
        parameters: dict[str, str | None] = {
            "path": None,
            "config": None
        }
        
        new_param: list[str] = []
        for value in values:
            if "=" in value:
                new_param.append(value) 

        get_parameters(new_param, parameters) 
        parameters['template'] = values[0]
        
        setattr(args, self.dest, ("generate", parameters))


class ValidateInitCommand(argparse.Action):
    def __call__(self, parser: Any, args: Any, values: str | Sequence[Any], option_string: Optional[str|None]=None) -> None: # type: ignore
        setattr(args, self.dest, ("init", values))

class ValidateUpdateCommand(argparse.Action):
    def __call__(self, parser: Any, args: Any, values: str | Sequence[Any], option_string: Optional[str|None]=None) -> None: # type: ignore
        setattr(args, self.dest, ("update", values))

class ValidateClearCacheCommand(argparse.Action):
    def __call__(self, parser: Any, args: Any, values: str | Sequence[Any], option_string: Optional[str|None]=None) -> None: # type: ignore
        setattr(args, self.dest, ("clear_cache", values))

#VALIDATION METHODS
def get_parameters(arg_values:Sequence[Any], parameters:dict[str, str | None]) -> None:
    
    valid_parameter_list = list(parameters.keys())
    for param in arg_values:
        # print(arg_values)
        parameter:str = ""
        value:str = ""

        try:
            parameter, value = param.split("=")
        except Exception:
            _exceptions.GenericException(f"Invalid parameter value pairing for argument {param}")

        if parameter not in valid_parameter_list:
            _exceptions.GenericException(f'Invalid parameter given "{parameter}". Must be one of: {valid_parameter_list}')
        parameters[parameter] = value
        # print(parameters)

def check_required_parameters(param:dict[str, str | None], required_parameters:list[str]) -> None:
    error_message = "Specify required parameters: "
    for parameter in required_parameters:
        if param[parameter] == None:
            error_message += parameter + ", "
            _exceptions.GenericException(error_message[:-2])

def check_file_param(file:str | None) -> None:
    #Check if yaml file ends in '*.yml' or '*.yaml'
    if file != None and (file[-4:].lower() == 'yaml' or file[-3:].lower() == 'yml'):
        #Looks ok, gave a YAML file
        pass
        #Check if file is readable
        if not os.path.isfile(file):
            _exceptions.GenericException(f'cannot read YAML file "{file}". Please verify path and filename.')