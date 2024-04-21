from fastapi import FastAPI

from controllers.earthquake_controller import router as earthquake_router

app = FastAPI()

app.include_router(earthquake_router)
