
HELP_GENERATE_MSG = """\
Create new SERFF microservices.
    Required parameters:
        [1] project = name of the project this microservice belongs to
        [2] service = name of this microservice
    Optional parameters:
        [1] runtime = options: nodejs and python (default: python)
        [2] file    = YAML file which holds the metadata of the domains included in this microservice. 
                        if not specified will generate a pristine SERFF"""

HELP_ADD_MODULE_MSG = """\
Add new modules for an existing microservice.
    Required Parameter:
        [1] YAML File = Metadata of the domain"""