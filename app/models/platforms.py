from tortoise import fields, models


class Platforms(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users", related_name="platforms")
    name = fields.CharField(max_length=100, null=False)
    description = fields.CharField(max_length=1000, null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
