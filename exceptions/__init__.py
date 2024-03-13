import sys
class GenericException():
    #TODO: Temporary exception to remove traceback for simplicity 
    def __init__(self, message:str, type:str ="ERROR"):
        print(f"[{type}]",message)
        sys.exit(1)