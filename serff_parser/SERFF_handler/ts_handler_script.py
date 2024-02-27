from __future__ import annotations
import helpers
import textwrap
from typing_extensions import Any
RUNTIME = "typescript"

import_strings = f"""
    import {{ APIGatewayProxyEvent, Context }} from "aws-lambda";
    import middy from "@middy/core";
    import {{ tracer, captureLambdaHandler }} from "../../../lib/commons/powertools";
    import {{ successResponse, errorResponse }} from "../../../lib/commons/response";
    import schemaValidator from "../_rules/schemas/validate";
    import policyValidator from "../_rules/policies/validate";
    import {{ connectionMiddleware, localMongoDBConnectionMiddleware }} from "../../../repositories/mongodb/_connection";"""

def generate_create_handler(module_name: str, module_attributes:dict[str, Any]):
    to_class_name = helpers.to_class(module_name)
    readable_var = helpers.to_readable_name(module_name)
    source_code = f"""\
    {import_strings}
    import schema from "../_rules/schemas/{to_class_name}/create";
    import {to_class_name}Controller from "../../../controllers/{to_class_name}Controller";
    import {{ writePolicy }} from "../_rules/policies/{to_class_name}";
    
    interface RequestParameter extends APIGatewayProxyEvent {{
        request: {{"""
    for attribute, attribute_items in module_attributes.items():
        if((helpers.get_fields(attribute_items.get('data_type', 'string'), RUNTIME)) == 'String'):
            data_type = (helpers.get_fields(attribute_items.get('data_type', 'string'), RUNTIME).lower())
        else: 
            data_type = (helpers.get_fields(attribute_items.get('data_type', 'string'), RUNTIME))

        field = helpers.to_camel_case(attribute)
        source_code += f"""
            {field}: {data_type};"""
    source_code += f"""
        }};
        requester: {{
            cognitoId: string;
            name: string;
            email: string;
            phone_number: string;
            role: string;
        }};
    }}

    const execute = async (
    event: RequestParameter,
    _context: Context
    ): Promise<Object> => {{
        try {{
            let controller = new {to_class_name}Controller();
            const data = await controller.create(event.request, event.requester);

            return successResponse({{
            message: "Successfully created {readable_var} data.",
            data,
            }});
        }} catch (error) {{
            return errorResponse(error);
        }}
    }};

    export const handler = middy(execute)
    //.use(captureLambdaHandler(tracer))
    //.use(policyValidator(writePolicy))
    .use(schemaValidator(schema))
    .use(localMongoDBConnectionMiddleware);
    """

    return textwrap.dedent(source_code)

def generate_get_handler(module_name: str, module_attributes:dict[str, Any]):
    class_name = helpers.convert_to_system_name(module_name, "class")
    to_class_name = helpers.to_class(module_name)
    source_code = f"""\
    {import_strings}
    import schema from "../_rules/schemas/{class_name}/get";
    import {{ readPolicy }} from "../_rules/policies/{class_name}";
    import {to_class_name}Controller from "../../../controllers/{to_class_name}Controller";
    
    interface RequestParameter extends APIGatewayProxyEvent {{
        request: {{
            id: string;
        }};
        requester: {{
            cognitoId: string;
            name: string;
            email: string;
            phone_number: string;
            role: string;
        }};
    }}

    const execute = async (
    event: RequestParameter,
    _context: Context
    ): Promise<Object> => {{
        try {{
            let controller = new {to_class_name}Controller();
            const data = await controller.find(event.request.id);

            return successResponse({{
                data,
            }});
        }} catch (error) {{
            return errorResponse(error);
        }}
    }};

    export const handler = middy(execute)
    //.use(captureLambdaHandler(tracer))
    //.use(policyValidator(readPolicy))
    .use(schemaValidator(schema))
    .use(localMongoDBConnectionMiddleware);
    """

    return textwrap.dedent(source_code)

def generate_list_handler(module_name: str, module_attributes:dict[str, Any]):
    class_name = helpers.convert_to_system_name(module_name, "class")
    to_class_name = helpers.to_class(module_name)
    source_code = f"""\
    {import_strings}
    import schema from "../_rules/schemas/{class_name}/list";
    import {{ listPolicy }} from "../_rules/policies/{class_name}";
    import {to_class_name}Controller from "../../../controllers/{to_class_name}Controller";


    interface RequestParameter extends APIGatewayProxyEvent {{
        request: {{
            page: number;
            pageSize: number;
            returnCount: boolean;
            likeFilters?: Array<{{
            keys: Array<string>;
            value: string;
            }}>;
            equalFilters?: Array<{{
            key: string;
            value: string;
            }}>;
            notEqualFilters?: Array<{{
            key: string;
            value: string;
            }}>;
            inFilters?: Array<{{
            key: string;
            value: Array<string>;
            }}>;
            notInFilters?: Array<{{
            key: string;
            value: Array<string>;
            }}>;
            betweenFilters?: Array<{{
            key: string;
            value: Array<any>;
            }}>;
            sorts?: Array<string>;
        }};
    }}

    const execute = async (
    event: RequestParameter,
    _context: Context
    ): Promise<Object> => {{
        try {{
            let controller = new {to_class_name}Controller();

            const data = await controller.paginate(event.request);

            return successResponse({{
                ...data,
            }});
        }} catch (error) {{
            return errorResponse(error);
        }}
    }};

    export const handler = middy(execute)
    //.use(captureLambdaHandler(tracer))
    //.use(policyValidator(listPolicy))
    .use(schemaValidator(schema))
    .use(localMongoDBConnectionMiddleware);
    """

    return textwrap.dedent(source_code)

def generate_update_handler(module_name: str, module_attributes:dict[str, Any]):
    class_name = helpers.convert_to_system_name(module_name, "class")
    to_class_name = helpers.to_class(module_name)
    readable_var = helpers.to_readable_name(module_name)
    source_code = f"""\
    {import_strings}
    import schema from "../_rules/schemas/{class_name}/update";
    import {{ patchPolicy }} from "../_rules/policies/{class_name}";
    import {to_class_name}Controller from "../../../controllers/{to_class_name}Controller";
    
    interface RequestParameter extends APIGatewayProxyEvent {{
        request: {{
            id: string;"""
    for attribute, attribute_items in module_attributes.items():
        if((helpers.get_fields(attribute_items.get('data_type', 'string'), RUNTIME)) == 'String'):
            data_type = (helpers.get_fields(attribute_items.get('data_type', 'string'), RUNTIME).lower())
        else: 
            data_type = (helpers.get_fields(attribute_items.get('data_type', 'string'), RUNTIME))

        field = helpers.to_camel_case(attribute)
        source_code += f"""
            {field}: {data_type};"""
    source_code += f"""
        }};
        requester: {{
            cognitoId: string;
            name: string;
            email: string;
            phone_number: string;
            role: string;
        }};
    }}

    const execute = async (
    event: RequestParameter,
    _context: Context
    ): Promise<Object> => {{
        try {{
            let controller = new {to_class_name}Controller();
            let {{ id, ...request }} = event.request;

            const data = await controller.update(id, request, event.requester);

            return successResponse({{
                message: "Successfully updated {readable_var} data.",
                data,
            }});
        }} catch (error) {{
            return errorResponse(error);
        }}
    }};

    export const handler = middy(execute)
    //.use(captureLambdaHandler(tracer))
    //.use(policyValidator(patchPolicy))
    .use(schemaValidator(schema))
    .use(localMongoDBConnectionMiddleware);
    """

    return textwrap.dedent(source_code)

def generate_delete_handler(module_name: str, module_attributes:dict[str, Any]):
    class_name = helpers.convert_to_system_name(module_name, "class")
    to_class_name = helpers.to_class(module_name)
    readable_var = helpers.to_readable_name(module_name)
    source_code = f"""\
    {import_strings}
    import schema from "../_rules/schemas/{class_name}/delete";
    import {{ deletePolicy }} from "../_rules/policies/{class_name}";
    import {to_class_name}Controller from "../../../controllers/{to_class_name}Controller";
    
    interface RequestParameter extends APIGatewayProxyEvent {{
        request: {{
            id: string;
        }};
        requester: {{
            cognitoId: string;
            name: string;
            email: string;
            phone_number: string;
            role: string;
        }};
    }}

    const execute = async (
    event: RequestParameter,
    _context: Context
    ): Promise<Object> => {{
        try {{
            let controller = new {to_class_name}Controller();
            await controller.delete(event.request.id, event.requester);

            return successResponse({{
            message: "Successfully deleted {readable_var} data.",
            }});
        }} catch (error) {{
            return errorResponse(error);
        }}
    }};

    export const handler = middy(execute)
    //.use(captureLambdaHandler(tracer))
    //.use(policyValidator(deletePolicy))
    .use(schemaValidator(schema))
    .use(localMongoDBConnectionMiddleware);
    """

    return textwrap.dedent(source_code)

def generate_search_handler(module_name: str, module_attributes:dict[str, Any]):
    class_name = helpers.convert_to_system_name(module_name, "class")
    to_class_name = helpers.to_class(module_name)
    source_code = f"""\
    {import_strings}
    import schema from "../_rules/schemas/{class_name}/search";
    import {{ listPolicy }} from "../_rules/policies/{class_name}";
    import {to_class_name}Controller from "../../../controllers/{to_class_name}Controller";
    
    interface RequestParameter extends APIGatewayProxyEvent {{
        request: {{
            limit: number;
            likeFilters?: Array<{{
                keys: Array<string>;
                value: string;
            }}>;
            equalFilters?: Array<{{
                key: string;
                value: string;
            }}>;
            notEqualFilters?: Array<{{
                key: string;
                value: string;
            }}>;
            inFilters?: Array<{{
                key: string;
                value: Array<string>;
            }}>;
            notInFilters?: Array<{{
                key: string;
                value: Array<string>;
            }}>;
            betweenFilters?: Array<{{
                key: string;
                value: Array<any>;
            }}>;
            sorts?: Array<string>;
        }};
    }}

    const execute = async (
    event: RequestParameter,
    _context: Context
    ): Promise<Object> => {{
        try {{
            let controller = new {to_class_name}Controller();

            const data = await controller.search(event.request);

            return successResponse({{
                data,
            }});
        }} catch (error) {{
            return errorResponse(error);
        }}
    }};

    export const handler = middy(execute)
    //.use(captureLambdaHandler(tracer))
    //.use(policyValidator(listPolicy))
    .use(schemaValidator(schema))
    .use(localMongoDBConnectionMiddleware);
    """

    return textwrap.dedent(source_code)