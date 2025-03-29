subjects_schema = {
    "type": "object",
    "required": ["data"],
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name", "regions"],
                "properties": {
                    "id": {"type": "integer", "minimum": 1, "maximum": 8},
                    "name": {
                        "type": "string",
                    },
                    "regions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["id", "name"],
                            "properties": {
                                "id": {
                                    "type": "integer",
                                },
                                "name": {
                                    "type": "string",
                                },
                            },
                        },
                    },
                },
            },
        }
    },
}

subjects_regions_schema = {
    "type": "object",
    "required": ["data"],
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": "string",
                    },
                },
            },
        },
    },
}

subjects_districts_schema = {
    "type": "object",
    "required": ["data"],
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": "string",
                    },
                },
            },
        },
    },
}
