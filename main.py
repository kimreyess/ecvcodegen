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
    "init":_construct.init,
    "generate":_construct.generate,
    "update":_construct.update
}

def run_parser() -> None:
    parser = argparse.ArgumentParser(
        description=_messages.DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('--init',
                        required=False,
                        nargs=0,
                        dest='construct',
                        action=_validation.ValidateInitCommand,
                        help=dedent(_help.HELP_INIT_MSG)
    )

    parser.add_argument('--generate',
                        required=False,
                        nargs="+",
                        dest='construct',
                        metavar=("{Boilerplate} path={path} config={config.json}"),
                        action=_validation.ValidateGenerateCommand,
                        help=dedent(_help.HELP_GENERATE_MSG)
    )

    parser.add_argument('--update',
                        required=False,
                        nargs=0,
                        dest='construct',
                        action=_validation.ValidateUpdateCommand,
                        help=dedent(_help.HELP_UPDATE_MSG)
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