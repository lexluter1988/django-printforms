from __future__ import annotations

import uuid as uuid

from django.db import models


class Timestamped(models.Model):
    """Abstract Model Class wth timestamp"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField("created", auto_now_add=True)
    modified_at = models.DateTimeField("changed", editable=False, auto_now=True)


class DefaultModel(Timestamped):
    """Abstract Model Class with uuid."""

    class Meta:
        abstract = True

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
