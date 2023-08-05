import pytest
from fastapi.testclient import TestClient

from ...utils import needs_pydanticv1


@pytest.fixture(name="client")
def get_client():
    from docs_src.path_operation_advanced_configuration.tutorial007 import app

    client = TestClient(app)
    return client


# TODO: pv2 add Pydantic v2 version
@needs_pydanticv1
def test_post(client: TestClient):
    yaml_data = """
        name: Deadpoolio
        tags:
        - x-force
        - x-men
        - x-avengers
        """
    response = client.post("/items/", content=yaml_data)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Deadpoolio",
        "tags": ["x-force", "x-men", "x-avengers"],
    }


# TODO: pv2 add Pydantic v2 version
@needs_pydanticv1
def test_post_broken_yaml(client: TestClient):
    yaml_data = """
        name: Deadpoolio
        tags:
        x - x-force
        x - x-men
        x - x-avengers
        """
    response = client.post("/items/", content=yaml_data)
    assert response.status_code == 422, response.text
    assert response.json() == {"detail": "Invalid YAML"}


# TODO: pv2 add Pydantic v2 version
@needs_pydanticv1
def test_post_invalid(client: TestClient):
    yaml_data = """
        name: Deadpoolio
        tags:
        - x-force
        - x-men
        - x-avengers
        - sneaky: object
        """
    response = client.post("/items/", content=yaml_data)
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {"loc": ["tags", 3], "msg": "str type expected", "type": "type_error.str"}
        ]
    }


# TODO: pv2 add Pydantic v2 version
@needs_pydanticv1
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.0.2",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "post": {
                    "summary": "Create Item",
                    "operationId": "create_item_items__post",
                    "requestBody": {
                        "content": {
                            "application/x-yaml": {
                                "schema": {
                                    "title": "Item",
                                    "required": ["name", "tags"],
                                    "type": "object",
                                    "properties": {
                                        "name": {"title": "Name", "type": "string"},
                                        "tags": {
                                            "title": "Tags",
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                    },
                                }
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            }
        },
    }
