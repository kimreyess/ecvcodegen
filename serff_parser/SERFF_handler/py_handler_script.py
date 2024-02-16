from __future__ import annotations

import helpers
import textwrap
from typing_extensions import Any
import_strings = f"""
    from app.rules.validator import validate_web_request
    from app.policies.validator import validate_role_permission

    from base_handlers.web import spawn_handler, app
    from base_handlers.database import initiate_database

    from helpers.monitoring import tracer, logger, metrics
    from helpers.response import SuccessResponse
"""

def generate_create_handler(module_name: str, module_attributes:dict[str, Any]) -> str:
    class_name = helpers.convert_to_system_name(module_name, "class")
    source_code = f"""\
    {import_strings}

    from app.policies.standard_policies import WritePolicy as policy
    from app.services.repositories.{module_name} import {class_name}, {class_name}Repository
    
    @tracer.capture_method
    def process():
        {module_name} = {class_name}({class_name}Repository(), app.validated_body)
        {module_name}.commit()
        {module_name}.repository.close_client()

        return SuccessResponse({module_name}.serialize(), "CREATE_SUCCESS")


    @validate_web_request(schema={class_name}.compose_schema())
    @validate_role_permission(policy=policy, module="{module_name}")
    @initiate_database(databases=["mongodb"])
    def handler(event, context):
        return spawn_handler(event, context, process)
    """

    return textwrap.dedent(source_code)

def generate_get_handler(module_name: str, module_attributes:dict[str, Any]):
    class_name = helpers.convert_to_system_name(module_name, "class")
    source_code = f"""\
    {import_strings}

    from app.policies.standard_policies import ReadPolicy as policy
    from app.services.repositories.{module_name} import {class_name}, {class_name}Repository
    
    @tracer.capture_method
    def process():
        {module_name} = {class_name}Repository().find_by_id(app.validated_body['{module_name}_id'])

        {module_name}.close_client()

        return SuccessResponse({module_name}.serialize(), "GET_BY_ID_SUCCESS")


    @validate_web_request(schema={class_name}.compose_schema(['id']))
    @validate_role_permission(policy=policy, module="{module_name}")
    @initiate_database(databases=["mongodb"])
    def handler(event, context):
        return spawn_handler(event, context, process)
    """

    return textwrap.dedent(source_code)

def generate_list_handler(module_name: str, module_attributes:dict[str, Any]):
    class_name = helpers.convert_to_system_name(module_name, "class")
    source_code = f"""\
    {import_strings}

    from app.policies.standard_policies import ListPolicy as policy
    from app.services.repositories.{module_name} import {class_name}, {class_name}Repository
    
    @tracer.capture_method
    def process():
        filter_by_roles = []
        {module_name} = {class_name}({class_name}Repository(), app.validated_body)
        response = {module_name}.list(app.validated_body)

        return SuccessResponse(**response)

    @validate_web_request(schema={class_name}.compose_schema("list"))
    @validate_role_permission(policy=policy, module="{module_name}")
    @initiate_database(databases=["mongodb"])
    def handler(event, context):
        return spawn_handler(event, context, process)
    """

    return textwrap.dedent(source_code)

def generate_update_handler(module_name: str, module_attributes:dict[str, Any]):
    class_name = helpers.convert_to_system_name(module_name, "class")
    source_code = f"""\
    {import_strings}

    from app.policies.standard_policies import PatchPolicy as policy
    from app.services.repositories.{module_name} import {class_name}, {class_name}Repository
    
    @tracer.capture_method
    def process():
        {module_name} = {class_name}Repository().find_by_id(app.validated_body['{module_name}_id'])
        app.validated_body.pop('{module_name}_id')
        {module_name}.update(app.validated_body)
        {module_name}.save()
        {module_name}.repository.close_client()

        return SuccessResponse({module_name}.serialize(), "EDIT_SUCCESS")


    @validate_web_request(schema={class_name}.compose_schema())
    @validate_role_permission(policy=policy, module="{module_name}")
    @initiate_database(databases=["mongodb"])
    def handler(event, context):
        return spawn_handler(event, context, process)
    """

    return textwrap.dedent(source_code)

def generate_delete_handler(module_name: str, module_attributes:dict[str, Any]):
    class_name = helpers.convert_to_system_name(module_name, "class")
    source_code = f"""\
    {import_strings}

    from app.policies.standard_policies import DeletePolicy as policy
    from app.services.repositories.{module_name} import {class_name}, {class_name}Repository
    
    @tracer.capture_method
    def process():
        {module_name} = {class_name}Repository().find_by_id(app.validated_body['{module_name}_id'])
        {module_name}.delete()
        {module_name}.repository.close_client()

        return SuccessResponse("Record deleted successfully", "DELETE_SUCCESS")


    @validate_web_request(schema={class_name}.compose_schema(['{module_name}_id']))
    @validate_role_permission(policy=policy, module="{module_name}")
    @initiate_database(databases=["mongodb"])
    def handler(event, context):
        return spawn_handler(event, context, process)
    """

    return textwrap.dedent(source_code)