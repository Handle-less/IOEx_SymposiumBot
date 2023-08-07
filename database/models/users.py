from tortoise import fields, models


class Users(models.Model):

    tg_id: fields.BigIntField = fields.BigIntField(
        unique=True
    )

    tg_username: fields.TextField = fields.TextField(
        null=True
    )

    tg_fullname: fields.TextField = fields.TextField(
        null=True
    )

    rank: fields.IntField = fields.IntField(
        default=0
    )

    role: fields.IntField = fields.IntField(
        default=0
    )
    # 1 - ; 2 - ; 3 - ; 4 - ; 5 - ; 6 - ; 7 - ;

    class Meta:
        table = 'users'
