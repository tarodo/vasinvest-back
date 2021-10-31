from tortoise import fields, models


class Currencies(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.Users", related_name="currencies.py", null=False
    )
    code = fields.CharField(max_length=10, null=False)
    name = fields.CharField(max_length=20, null=True)
    is_main = fields.BooleanField(null=False, default=False)
