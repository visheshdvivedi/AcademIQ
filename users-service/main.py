from sqlalchemy import exc

from fastapi import FastAPI

from routes import router
from utils.database import Base, engine
from utils.exception_handling import (
    request_validation_error_handler, RequestValidationError,
    integrity_error_handler, IntegrityError,
    data_error_handler, DataError
)

# database configurations
Base.metadata.create_all(bind=engine)

# creating app
app = FastAPI()
app.include_router(router)

# add global exception handlers
app.add_exception_handler(DataError, data_error_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)