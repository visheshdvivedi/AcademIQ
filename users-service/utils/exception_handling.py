from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from starlette import status
from sqlalchemy.exc import DataError, IntegrityError

# ----- Global exception handlers -----

async def request_validation_error_handler(request: Request, exception: RequestValidationError):
    response = []

    for err in exception.errors():
        response.append({
            "type": err['type'],
            'param': err['loc'][-1],
            'message': err['msg']
        })

    return JSONResponse(
        status_code=400,
        content={"detail": response}
    )

# ----- Route exception handlers -----

def integrity_error_handler(exception: IntegrityError):
    if "users_email_key" in exception.orig.args[0]:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Email ID already exists, please login to continue"}
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Unknown integrity error"}
    )

def data_error_handler(exception: DataError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exception.orig)}
    )

def default_exception_handler(exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An error occured"}
    )