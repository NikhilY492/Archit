MIRRORED_CUPBOARD_SCHEMA = {
    "type": "object",
    "required": ["dimensions", "parameters"],
    "properties": {
        "dimensions": {
            "type": "object",
            "required": ["width", "height", "depth"],
            "properties": {
                "width": {"type": "number", "minimum": 1},
                "height": {"type": "number", "minimum": 1},
                "depth": {"type": "number", "minimum": 0.5}
            },
            "additionalProperties": False
        },
        "parameters": {
            "type": "object",
            "required": ["door_type", "mirror"],
            "properties": {
                "door_type": {
                    "type": "string",
                    "enum": ["sliding", "swing"]
                },
                "mirror": {
                    "type": "boolean"
                }
            },
            "additionalProperties": False
        }
    },
    "additionalProperties": False
}
