from enum import Enum

from tortoise import fields, models


class TickerTypesEnum(Enum):
    crypto = 'crypto'
    share = 'share'


class Tickers(models.Model):
    id = fields.IntField(pk=True)
    platform = fields.ForeignKeyField("models.Platforms", related_name="tickers", null=False)
    code = fields.CharField(max_length=20, null=False)
    name = fields.CharField(max_length=100, null=True)
    description = fields.CharField(max_length=1000, null=True)
    type = fields.CharEnumField(TickerTypesEnum, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
