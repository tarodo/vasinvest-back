from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=100, unique=True)
    full_name = fields.CharField(max_length=100, null=True)
    hashed_password = fields.CharField(max_length=128, null=False)
    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
