from typing import Optional
from pydantic import BaseModel

"""
"name": "Президент Российской Федерации",
"short_name": "Президент Российской Федерации",
"external_id": "e94b6872-dcac-414f-b2f1-a538d13a12a0",
"code": "president",
"has_children": false,
"parent_id": null,
"categories": null
"""


class OrganSchema(BaseModel):
    name: str
    short_name: str
    external_id: str
    code: str
    parent_id: Optional[str]
