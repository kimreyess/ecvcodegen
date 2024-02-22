from typing_extensions import Any 
import helpers
def generate_lambda_create_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  Create{helpers.to_class(module_name)}:
    handler: app/handlers/http/{module_name}/create_{module_name}_handler.handler
    events:
      - http:
          path: /
          method: post
          cors: true
          # authorizer: # uncomment for auth
          #   type: COGNITO_USER_POOLS
          #   authorizerId:
          #     Ref: ApiGatewayAuthorizer
          #   scopes:
          #     - aws.cognito.signin.user.admin
          #     - developer/access
          #     - email
    # warmup: 
    #   peakWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    #   offWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    """
    return source_code

def generate_lambda_update_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  Update{helpers.to_class(module_name)}:
    handler: app/handlers/http/{module_name}/update_{module_name}_handler.handler
    events:
      - http:
          path: /{{id}}
          method: patch
          cors: true
          # authorizer: # uncomment for auth
          #   type: COGNITO_USER_POOLS
          #   authorizerId:
          #     Ref: ApiGatewayAuthorizer
          #   scopes:
          #     - aws.cognito.signin.user.admin
          #     - developer/access
          #     - email
    # warmup: 
    #   peakWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    #   offWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    """
    return source_code


def generate_lambda_list_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  List{helpers.to_class(module_name)}:
    handler: app/handlers/http/{module_name}/list_{module_name}_handler.handler
    events:
      - http:
          path: /list/
          method: post
          cors: true
          # authorizer: # uncomment for auth
          #   type: COGNITO_USER_POOLS
          #   authorizerId:
          #     Ref: ApiGatewayAuthorizer
          #   scopes:
          #     - aws.cognito.signin.user.admin
          #     - developer/access
          #     - email
    # warmup: 
    #   peakWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    #   offWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    """
    return source_code

def generate_lambda_get_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  Get{helpers.to_class(module_name)}:
    handler: app/handlers/http/{module_name}/get_{module_name}_handler.handler
    events:
      - http:
          path: /{{id}}
          method: get
          cors: true
          # authorizer: # uncomment for auth
          #   type: COGNITO_USER_POOLS
          #   authorizerId:
          #     Ref: ApiGatewayAuthorizer
          #   scopes:
          #     - aws.cognito.signin.user.admin
          #     - developer/access
          #     - email
    # warmup: 
    #   peakWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    #   offWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    """
    return source_code

def generate_lambda_delete_handler_iac_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    
    ##NOTE: Maintain the indentation
    source_code:str =f"""
  Delete{helpers.to_class(module_name)}:
    handler: app/handlers/http/{module_name}/delete_{module_name}_handler.handler
    events:
      - http:
          path: /{{id}}
          method: delete
          cors: true
          # authorizer: # uncomment for auth
          #   type: COGNITO_USER_POOLS
          #   authorizerId:
          #     Ref: ApiGatewayAuthorizer
          #   scopes:
          #     - aws.cognito.signin.user.admin
          #     - developer/access
          #     - email
    # warmup: 
    #   peakWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    #   offWarmerLow:
    #     enabled: ${{self:custom.isWarmUpEnabled.${{self:provider.stage}}.isEnabled}}
    """
    return source_code