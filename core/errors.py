from fastapi import HTTPException

class MisconfiguredError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)

class ExternalServiceError(HTTPException):
    def __init__(self, detail: str = "External service error"):
        super().__init__(status_code=502, detail=detail)
