from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_app_includes_all_routers():
    """
    Test that the app includes all the routers.
    """
    expected_routes = [
        "/v1/earthquakes/{city_id}",
        "/v1/cities/",
        "/v1/countries/",
        "/v1/states/",
    ]
    actual_routes = [route.path for route in app.routes]
    for route in expected_routes:
        assert (
            route in actual_routes
        ), f"Route {route} not found in the registered routes."
