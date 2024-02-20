from __future__ import annotations

import helpers
import textwrap
from typing_extensions import Any
import_strings = f"""
    import {{ APIGatewayProxyEvent, Context }} from "aws-lambda";
    import middy from "@middy/core";
    import {{ tracer, captureLambdaHandler }} from "../../../lib/commons/powertools";
    import {{ successResponse, errorResponse }} from "../../../lib/commons/response";
    import schemaValidator from "../_rules/schemas/validate";
    import policyValidator from "../_rules/policies/validate";
    import {{ connectionMiddleware }} from "../../../repositories/mongodb/_connection";
"""

def generate_rule_policies_handler(module_name: str, module_attributes:dict[str, Any]):
    module = helpers.to_camel_case(module_name)
    source_code = f"""\
        export const writePolicy = ["*:*", "{module}s:*", "{module}s:write"];
        export const readPolicy = ["*:*", "{module}s:*", "{module}s:read"];
        export const patchPolicy = ["*:*", "{module}s:*", "{module}s:patch"];
        export const deletePolicy = ["*:*", "{module}s:*", "{module}s:delete"];
    """

    return textwrap.dedent(source_code)
    class_name = helpers.convert_to_system_name(module_name, "class")
    source_code = f"""\
    {import_strings}
    import schema from "../_rules/schemas/{class_name}/create";
    import {{ deletePolicy }} from "../_rules/policies/{class_name}";
    import {module_name}Controller from "../../../controllers/{module_name}Controller";
    
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
            let controller = new {module_name}Controller();
            await controller.delete(event.request.id, event.requester);

            return successResponse({{
            message: "Successfully deleted {class_name} data.",
            }});
        }} catch (error) {{
            return errorResponse(error);
        }}
    }};

    export const handler = middy(execute)
    .use(captureLambdaHandler(tracer))
    .use(policyValidator(deletePolicy))
    .use(schemaValidator(schema))
    .use(connectionMiddleware);
    """

    return textwrap.dedent(source_code)