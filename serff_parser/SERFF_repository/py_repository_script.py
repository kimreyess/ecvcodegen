import textwrap
from typing_extensions import Any 
import helpers

def generate_repository_source_code(module_name:str, module_attributes:dict[str, Any])->str:
    class_name: str = helpers.convert_to_system_name(module_name, "class")
    source_code:str = f"""\
    import app.domain.{module_name}

    class {class_name}Repository(MongoDBBaseRepository):
        COLLECTION_NAME = {module_name}
    """

    return textwrap.dedent(source_code)