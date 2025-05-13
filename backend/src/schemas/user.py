from .base import BaseSchema
from .role import RoleSchema


class UserSchema(BaseSchema):
    username: str
    email: str
    role: RoleSchema


class UserRequestSchema(UserSchema):
    password: str


class UserInsertSchema(UserSchema):
    hashed_password: str


class UserResponseSchema(UserSchema):
    id: int
