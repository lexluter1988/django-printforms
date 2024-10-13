from __future__ import annotations

import uuid


class ContentTemplateError(Exception):
    """Base class for exceptions."""


class ContentTemplateNotFound(ContentTemplateError):
    def __init__(self, content_template_uuid: uuid.UUID) -> None:
        super().__init__(f"Template [{content_template_uuid}] not found")
