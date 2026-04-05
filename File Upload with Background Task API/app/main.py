from fastapi import FastAPI
from app.api.routes import router
from app.core.config import APP_NAME, VERSION


app = FastAPI(
    title = APP_NAME,
    version=VERSION
)

app.include_router(router, prefix="/auth")