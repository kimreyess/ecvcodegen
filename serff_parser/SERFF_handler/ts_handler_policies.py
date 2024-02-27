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
        export const writePolicy = ["*:*", "{module}:*", "{module}:write"];
        export const readPolicy = ["*:*", "{module}:*", "{module}:read"];
        export const patchPolicy = ["*:*", "{module}:*", "{module}:patch"];
        export const deletePolicy = ["*:*", "{module}:*", "{module}:delete"];
        export const listPolicy = ["*:*", "{module}:*", "{module}:list"];
    """

    return textwrap.dedent(source_code)
