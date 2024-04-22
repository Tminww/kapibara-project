from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str
    email: str


class UserRequestSchema(UserBaseSchema):
    password: str


class UserInsertSchema(UserBaseSchema):
    hashed_password: str


class GetUserSchema(UserBaseSchema):
    id: int
