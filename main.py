import argparse
from textwrap import dedent
from typing_extensions import Any
# import os
import validation as _validation
import construct as _construct
# import exceptions as _exception
import messages as _messages
import messages.help as _help

CONSTRUCTS:dict[str, Any]= {
    "generate":_construct.generate,
    "add-module":_construct.add_module,
    "project_init":_construct.project_init
}

def run_parser() -> None:
    parser = argparse.ArgumentParser(
        description=_messages.DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('--generate',
                        required=False,
                        dest='construct',
                        nargs="+",
                        metavar=("project={Project Name} service={Service Name}", "file, runtime"),
                        action=_validation.ValidateGenerateCommand,
                        help=dedent(_help.HELP_GENERATE_MSG)
    )

    parser.add_argument('--add-module',
                        required=False,
                        nargs=1,
                        dest='construct',
                        action=_validation.ValidateAddModuleCommand,
                        metavar=('{YAML File}'),
                        help=dedent(_help.HELP_ADD_MODULE_MSG)
    )
    
    parser.add_argument('--project-init',
                        required=False,
                        nargs=0,
                        dest='construct',
                        action=_validation.ValidateProjectInitCommand,
                        help=dedent(_help.HELP_PROJECT_INIT_MSG)
    )

    args = parser.parse_args()

    if args.construct:
        # constructs created, proceed on parsing the yaml file if specified
        construct_type, parameters = args.construct
        CONSTRUCTS[construct_type](parameters)
    else:
        # if no argument passed, display banner 
        print(dedent(_messages.BANNER))
        exit(1)

#NOTE: For development mode. Run the script using python main.py
if __name__ == "__main__":
    run_parser()