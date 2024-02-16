from typing_extensions import Optional,Sequence, Any
import argparse
import os
import exceptions as _exceptions


# VALIDATION CLASSES
class ValidateGenerateCommand(argparse.Action):
    REQUIRED_PARAMETERS:list[str] = ["project", "service"]
    VALID_RUNTIME:list[str]       = ["python", "typescript"]
    DEFAULT_RUNTIME: str          = "python"
    
    def __call__(self, parser: Any, args: Any, values:Sequence[Any], option_string: Optional[str|None]=None) -> None: # type: ignore
        parameters = {
            "project": None,
            "service": None,
            "file"   : None,
            "runtime": ValidateGenerateCommand.DEFAULT_RUNTIME 
        }
        get_parameters(values, parameters)
        check_required_parameters(parameters, ValidateGenerateCommand.REQUIRED_PARAMETERS)
        check_file_param(parameters["file"])

        setattr(args, self.dest, ("generate", parameters))

class ValidateAddModuleCommand(argparse.Action):
    def __call__(self, parser: Any, args: Any, values: str | Sequence[Any], option_string: Optional[str|None]=None) -> None: # type: ignore
        filename:str = values # type: ignore
        check_file_param(filename)  
        setattr(args, self.dest, ("add_module", values))

#VALIDATION METHODS
def get_parameters(arg_values:Sequence[Any], parameters:dict[str, str | None]) -> None:
    
    valid_parameter_list = list(parameters.keys())
    for param in arg_values:
        parameter:str = ""
        value:str = ""

        try:
            parameter, value = param.split("=")
        except Exception:
            _exceptions.GenericException(f"Invalid parameter value pairing for argument {param}")

        if parameter not in valid_parameter_list:
            _exceptions.GenericException(f'Invalid parameter given "{parameter}". Must be one of: {valid_parameter_list}')
        parameters[parameter] = value

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