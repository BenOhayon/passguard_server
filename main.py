from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from db.db_connector import connect_db
from model.exceptions import PassGuardAPIException
from routes.base_route import base_router

app = FastAPI(
    title="PassGuard Server",
    version="1.0.0"
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

connect_db(lambda: print("Pinged your deployment. You successfully connected to MongoDB!"))
app.include_router(base_router, prefix='/api')


@app.exception_handler(PassGuardAPIException)
def exception_handler(_: Response, e: PassGuardAPIException):
    return JSONResponse(
        status_code=e.status_code,
        content={"error": e.error_message}
    )
