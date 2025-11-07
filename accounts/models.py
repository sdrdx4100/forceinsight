from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', '管理者'
        DATA_STEWARD = 'data_steward', 'データ管理者'
        ANALYST = 'analyst', 'アナリスト'
        VIEWER = 'viewer', 'ビューア'

    role = models.CharField(
        max_length=32,
        choices=Roles.choices,
        default=Roles.VIEWER,
        help_text='ユーザーのロールを表します。アクセス制御と承認フローに利用します。'
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"
