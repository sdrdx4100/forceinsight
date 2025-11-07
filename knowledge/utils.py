from __future__ import annotations

from typing import Any

from django.contrib.contenttypes.models import ContentType

from .models import UsageLog


def log_usage(user, *, action: str, target, context: dict[str, Any] | None = None) -> UsageLog:
    """操作履歴を保存するヘルパー。"""
    if user.is_anonymous:
        raise ValueError('匿名ユーザーはログ対象外です。')
    content_type = ContentType.objects.get_for_model(target.__class__)
    return UsageLog.objects.create(
        user=user,
        action=action,
        target_type=content_type,
        target_id=target.pk,
        context=context or {},
    )
