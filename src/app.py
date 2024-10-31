from fastapi import FastAPI

from api.auth.routes import router as auth_router

fast_api = FastAPI()
fast_api.include_router(auth_router)
