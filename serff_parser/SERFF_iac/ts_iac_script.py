from typing_extensions import Any 
import helpers
def generate_lambda_create_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  Create{helpers.to_class(module_name)}:
    handler: app/handlers/http/{helpers.to_class(module_name)}/create.handler
    events:
      - http:
          path: /{helpers.to_class(module_name)}/create
          method: post
          cors: true
          # Uncomment this if you wish to attach an authorizer for your functions
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId:
              Ref: ApiGatewayAuthorizer
    """
    return source_code

def generate_lambda_update_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  Update{helpers.to_class(module_name)}:
    handler: app/handlers/http/{helpers.to_class(module_name)}/update.handler
    events:
      - http:
          path: /{helpers.to_class(module_name)}/{{id}}
          method: patch
          cors: true
          # Uncomment this if you wish to attach an authorizer for your functions
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId:
              Ref: ApiGatewayAuthorizer
    """
    return source_code


def generate_lambda_list_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  List{helpers.to_class(module_name)}:
    handler: app/handlers/http/{helpers.to_class(module_name)}/list.handler
    events:
      - http:
          path: /{helpers.to_class(module_name)}/list
          method: post
          cors: true
          # Uncomment this if you wish to attach an authorizer for your functions
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId:
              Ref: ApiGatewayAuthorizer
    """
    return source_code

def generate_lambda_get_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  Get{helpers.to_class(module_name)}:
    handler: app/handlers/http/{helpers.to_class(module_name)}/get.handler
    events:
      - http:
          path: /{helpers.to_class(module_name)}/{{id}}
          method: get
          cors: true
          # Uncomment this if you wish to attach an authorizer for your functions
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId:
              Ref: ApiGatewayAuthorizer
    """
    return source_code

def generate_lambda_delete_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  Delete{helpers.to_class(module_name)}:
    handler: app/handlers/http/{helpers.to_class(module_name)}/delete.handler
    events:
      - http:
          path: /{helpers.to_class(module_name)}/{{id}}
          method: delete
          cors: true
          # Uncomment this if you wish to attach an authorizer for your functions
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId:
              Ref: ApiGatewayAuthorizer
    """
    return source_code

def generate_lambda_search_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  Search{helpers.to_class(module_name)}:
    handler: app/handlers/http/{helpers.to_class(module_name)}/search.handler
    events:
      - http:
          path: /{helpers.to_class(module_name)}/search
          method: post
          cors: true
          # Uncomment this if you wish to attach an authorizer for your functions
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId:
              Ref: ApiGatewayAuthorizer
    """
    return source_code