from tortoise import fields, models


class Currencies(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.Users", related_name="currencies.py", null=False
    )
    code = fields.CharField(max_length=10, null=False)
    name = fields.CharField(max_length=40, null=True)
    is_main = fields.BooleanField(null=False, default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
