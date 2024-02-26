import textwrap
from typing_extensions import Any 
import helpers

def generate_repository_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    class_name: str = helpers.convert_to_system_name(module_name, "class")
    source_code:str = f"""\
    from app.services.repositories.base_repositories.mongodb_base_repository import MongodbBaseRepository
    from app.domains.{module_name}.list_{module_name} import {class_name}, {class_name}List
    from app.exceptions.exception_handlers import NoRecordsFoundException
    
    from typing_extensions import Any 

    class {class_name}Repository(MongodbBaseRepository):
        
        def __init__(self)->None:
        
            self.COLLECTION_NAME = '{module_name}'
            self.DOMAIN_OBJECT = {class_name}
            self.DOMAIN_COLLECTION = {class_name}List

        @classmethod
        def list_{module_name}(cls, data:dict[str, Any])-> dict[str, Any]:
        
            filter = {{
                "$and": [
                    {{"deleted_at": {{"$eq": None}}}}
                ] 
        }}
            if "search_val" in list(data.keys()):
                search_value:dict[str, str] = {{"$regex": data["search_val"], "$options": "i"}}
                search_filter:dict[str, Any] = {{
                    "$or": ["""
    for attribute_name, attribute_items in module_attributes.items(): #type: ignore
        source_code += f"""
                            {{"{attribute_name}": search_value}},"""
    source_code +=f"""
                    ]
                }}
                filter["$and"].append(search_filter) 
     
            sort_order = {{}}
            if "sort_field" in list(data.keys()):
                sort_order[data['sort_field']] = data.get("sort_order", "ASCENDING")
            else:
                sort_order["created_at"] = "ASCENDING"
            
            pagination:dict [str, str] = {{
                "page": data["page"],
                "page_size": data["page_size"]
            }}   
            result, return_count = cls.where(query_input=filter, sort_input=sort_order, pagination=pagination, override= True, return_count = True) #type: ignore
        
            # self.close_client()
            result: list[dict[str, Any]] = result.serialize() #type: ignore
            return_dict:dict[str, Any] = {{}}
            total_records = len(result) #type: ignore
            if total_records > 0:
                return_dict["data"] = result
                return_dict["return_count"] = return_count
                return_dict["return_count"]["current_page_count"] = total_records
            else:
                raise NoRecordsFoundException

            return return_dict
    """

    return textwrap.dedent(source_code)