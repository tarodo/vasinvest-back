from tortoise import fields, models


class Activities(models.Model):
    id = fields.IntField(pk=True)
    ticker = fields.ForeignKeyField(
        "models.Tickers", related_name="activities", null=False
    )
    datetime = fields.DatetimeField(null=False)
    amount = fields.FloatField(null=False)
    expenses = fields.FloatField(null=False)
    currency = fields.ForeignKeyField("models.Currencies", null=False)
