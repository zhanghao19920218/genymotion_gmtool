# coding: utf-8
from enum import Enum

class GmtoolErrorType(Enum):
    NotFoundDevice = 1
    
    Others = 2

class GmtoolError(Exception):
    """The error from gmtool

    Args:
        Exception (_type_): _description_
    """
    message: str = ""
    
    error_type: GmtoolErrorType = GmtoolErrorType.Others
    
    
    def __init__(self,
                 error_type: GmtoolErrorType,
                 message: str = ""):
        self.error_type = error_type
        self.message = message