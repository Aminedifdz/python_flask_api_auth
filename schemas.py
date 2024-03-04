from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.String()
    username = fields.String()
    email = fields.String()

