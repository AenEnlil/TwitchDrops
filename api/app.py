from fastapi import FastAPI

from .api_router import api_router


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(api_router)

    @application.get('/')
    async def root():
        return {'message': 'Hello world'}

    return application


app = get_application()

