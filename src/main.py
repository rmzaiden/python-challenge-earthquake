from dotenv import load_dotenv
from fastapi import FastAPI

from controllers.city_controller import city_router as city_router
from controllers.country_controller import country_router
from controllers.earthquake_controller import earthquake_router
from controllers.earthquake_controller import \
    earthquake_router as earthquake_router
from controllers.state_controller import state_router

load_dotenv()

app = FastAPI()

app.include_router(earthquake_router)
app.include_router(city_router)
app.include_router(country_router)
app.include_router(state_router)
