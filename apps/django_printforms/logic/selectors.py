from __future__ import annotations

import typing

from apps.django_printforms.models import ContentTemplate

if typing.TYPE_CHECKING:  # pragma: no cover
    import uuid

    from django.db.models import QuerySet


def content_templates__all() -> QuerySet[ContentTemplate]:
    return ContentTemplate.objects.all()


def content_template__by_id(*, template_id: int) -> ContentTemplate:
    return content_templates__all().get(id=template_id)


def content_template__find_by_uuid(
    *, content_template_uuid: uuid.UUID
) -> ContentTemplate | None:
    return content_templates__all().filter(uuid=content_template_uuid).first()


def content_template__find_by_code(*, code: str) -> ContentTemplate:
    return content_templates__all().get(code__exact=code)
