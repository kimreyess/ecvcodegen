import textwrap
from typing_extensions import Any

import helpers

def generate_controller_source_code(module_name:str, module_attributes:dict[str, Any]):
    class_name = helpers.to_class(module_name)
    class_name_lowercase = helpers.to_camel_case(module_name)
    
    source_code = f"""\
    import CognitoIdentityServiceProvider from "../services/aws/cognito";
    import CreateAdminAuditLogEvent from "../emitters/create-admin-audit-log";
    import {{ generateRandomString }} from "../lib/helpers/randomizer";
    import {{ getCurrentDateTime }} from "../lib/helpers/datetime";
    import {class_name}Repository from "../repositories/mongodb/{class_name}Repository";
    import {{ EmailException, ResourceNotFoundException, UnauthorizedAccessException, }} from "../lib/commons/exceptions";

    interface RequesterInterface {{
        cognitoId: string;
        name: string;
        role: string;
        email?: string;
        phone_number?: string;
    }}

    interface FiltersInterface {{
        limit?: number;
        page?: number;
        pageSize?: number;
        returnCount?: boolean;
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
    }}

    class {class_name}Controller {{"""

    #ADD
    source_code += f"""
        async create(
            payload: {{"""
    for attribute, attribute_items in module_attributes.items():
            if(attribute_items.get("data_type", "class") == 'date'):
                data_type = 'Date'
            elif(attribute_items.get("data_type", "class") == 'class'):
                data_type = 'string'
            elif(attribute_items.get("data_type", "class") == 'int'):
                data_type = 'number'
            elif(attribute_items.get("data_type", "class") == 'file-upload'):
                data_type = 'string'
            else:
                data_type = attribute_items.get("data_type", "class")
            

            field = helpers.to_camel_case(attribute)
            source_code += f"""
                {field}: {data_type};"""   
    source_code += f"""
            }},
            requester: RequesterInterface = {{
                cognitoId: "SYS",
                name: "System Generated",
                role: "SYS",
            }}
        ): Promise<object> {{
            const {class_name_lowercase} = new {class_name}Repository();

            const requesterDetails = {{
                createdBy: requester.name,
                createdByCognitoId: requester.cognitoId,
                createdAt: getCurrentDateTime(),
            }};

            const result = await {class_name_lowercase}.save({{
                ...payload,
                ...requesterDetails,
            }});

            const auditLog = {{
                moduleId: result._id,
                module: "{class_name_lowercase}",
                service: process.env["SERVICE_NAME"] || "N/A",
                type: "create",
                reference: "Create {class_name_lowercase} Package Data",
                ...requesterDetails,
            }};

            const updated = await {class_name_lowercase}.update(result._id, {{
                $push: {{
                    logs: {{
                        $each: [auditLog], // Element to be added
                        $position: 0, // Position at the beginning
                    }},
                }},
            }});

            const createAuditLogEvent = new CreateAdminAuditLogEvent();
            await createAuditLogEvent.process({{
                ...auditLog,
                eventData: payload,
                previousData: {{}},
            }});

            return updated;
        }}
        """


    #EDIT
    source_code += f"""
        async update(
            id: string,
            payload: {{"""
    for attribute, attribute_items in module_attributes.items():
            if(attribute_items.get("data_type", "class") == 'date'):
                data_type = 'Date'
            elif(attribute_items.get("data_type", "class") == 'class'):
                data_type = 'string'
            elif(attribute_items.get("data_type", "class") == 'int'):
                data_type = 'number'
            elif(attribute_items.get("data_type", "class") == 'file-upload'):
                data_type = 'string'
            else:
                data_type = attribute_items.get("data_type", "class")
            

            field = helpers.to_camel_case(attribute)
            source_code += f"""
                {field}: {data_type};"""   
    source_code += f"""
            }},
            requester: RequesterInterface = {{
                cognitoId: "SYS",
                name: "System Generated",
                role: "SYS",
            }}
        ): Promise<object> {{
            const {class_name_lowercase} = new {class_name}Repository();

            const previousData = await {class_name_lowercase}.find(
                id, "_id""" 
    for attribute, attribute_items in module_attributes.items():
            field = helpers.to_camel_case(attribute)
            source_code += f""" {field}"""   
    source_code += f"""\"
            );

            const requesterDetails = {{
                createdBy: requester.name,
                createdByCognitoId: requester.cognitoId,
                createdAt: getCurrentDateTime(),
            }};

            const result = await {class_name_lowercase}.save({{
                ...payload,
                ...requesterDetails,
            }});

            const auditLog = {{
                moduleId: result._id,
                module: "{class_name_lowercase}",
                service: process.env["SERVICE_NAME"] || "N/A",
                type: "create",
                reference: "Create {class_name_lowercase} Package Data",
                ...requesterDetails,
            }};

            const updated = await {class_name_lowercase}.update(result._id, {{
                $push: {{
                    logs: {{
                        $each: [auditLog], // Element to be added
                        $position: 0, // Position at the beginning
                    }},
                }},
            }});

            const createAuditLogEvent = new CreateAdminAuditLogEvent();
            await createAuditLogEvent.process({{
                ...auditLog,
                eventData: payload,
                previousData: {{}},
            }});

            return updated;
        }}
        """

    #FIND
    source_code += f"""
        async find(id: string): Promise<{{"""
    for attribute, attribute_items in module_attributes.items():
            if(attribute_items.get("data_type", "class") == 'date'):
                data_type = 'Date'
            elif(attribute_items.get("data_type", "class") == 'class'):
                data_type = 'string'
            elif(attribute_items.get("data_type", "class") == 'int'):
                data_type = 'number'
            elif(attribute_items.get("data_type", "class") == 'file-upload'):
                data_type = 'string'
            else:
                data_type = attribute_items.get("data_type", "class")
            

            field = helpers.to_camel_case(attribute)
            source_code += f"""
                {field}: {data_type};"""   
    source_code += f"""
                logs: string;
        }}> {{
            const {class_name_lowercase} = new {class_name}Repository();

            return await {class_name_lowercase}.find(
                id, "_id""" 
    for attribute, attribute_items in module_attributes.items():
            field = helpers.to_camel_case(attribute)
            source_code += f""" {field}"""   
    source_code += f""" logs"
            );
        }}
    """

    #DELETE
    source_code += f"""
        async delete(
            id: string,
            requester: RequesterInterface = {{
                cognitoId: "SYS",
                name: "System Generated",
                role: "SYS",
            }}
        ): Promise<void> {{
            const {class_name_lowercase} = new {class_name}Repository();

            const previousData = await {class_name_lowercase}.find(
                id, "_id""" 
    for attribute, attribute_items in module_attributes.items():
            field = helpers.to_camel_case(attribute)
            source_code += f""" {field}"""   
    source_code += f"""\"
            );

            const requesterDetails = {{
                createdBy: requester.name,
                createdByCognitoId: requester.cognitoId,
                createdAt: getCurrentDateTime(),
            }};

            const auditLog = {{
                moduleId: id,
                module: "option",
                service: process.env["SERVICE_NAME"] || "N/A",
                type: "delete",
                eventData: {{
                    id,
                }},
                previousData,
                reference: "Delete Option Data",
                ...requesterDetails,
            }};

            await {class_name_lowercase}.delete(id);

            const createAuditLogEvent = new CreateAdminAuditLogEvent();
            await createAuditLogEvent.process(auditLog);
        }}
    """

    
    #PAGINATE
    source_code += f"""
        async paginate(payload: FiltersInterface): Promise<object> {{
            let {{ page, pageSize, returnCount, ...filters }} = payload;

            const {class_name_lowercase} = new {class_name}Repository();

            return await {class_name_lowercase}.paginate(
                page,
                pageSize,
                returnCount,
                filters, "_id""" 
    for attribute, attribute_items in module_attributes.items():
            field = helpers.to_camel_case(attribute)
            source_code += f""" {field}"""   
    source_code += f""" createdAt createdBy createdByCognitoId updatedAt updatedBy updatedByCognitoId"
            );
        }}
    """

    #SEARCH/ALL
    source_code += f"""
        async search(payload: FiltersInterface): Promise<object> {{
            let {{ limit, ...filters }} = payload;

            const {class_name_lowercase} = new {class_name}Repository();

            return await {class_name_lowercase}.all(
                filters,
                limit, "_id""" 
    for attribute, attribute_items in module_attributes.items():
            field = helpers.to_camel_case(attribute)
            source_code += f""" {field}"""   
    source_code += f""" createdAt createdBy createdByCognitoId updatedAt updatedBy updatedByCognitoId"
            );
        }}
    """

    source_code += f"""
    }}

    export default {class_name}Controller;
    """

    return textwrap.dedent(source_code)