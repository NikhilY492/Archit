from jsonschema import validate, ValidationError
from fastapi import HTTPException
from app.core.schemas.registry import COMPONENT_SCHEMAS

def validate_component_payload(component_type: str, dimensions: dict, parameters: dict):
    schema = COMPONENT_SCHEMAS.get(component_type)

    if not schema:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported component_type: {component_type}"
        )

    try:
        validate(
            instance={
                "dimensions": dimensions,
                "parameters": parameters
            },
            schema=schema
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Component schema validation failed: {e.message}"
        )
