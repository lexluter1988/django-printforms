from __future__ import annotations

import os
import typing

from django.conf import settings
from weasyprint import HTML

from django_printforms.exceptions import ContentTemplateNotFound
from django_printforms.logic.selectors import content_template__find_by_uuid
from django_printforms.models import ContentTemplate

if typing.TYPE_CHECKING:
    import uuid

BASE_DIR = os.path.join(settings.BASE_DIR, "content_templates")


def content_template__create_pdf_from_html_str(
    *, string_html: str, base_url: str = BASE_DIR
) -> HTML:
    """
    Generates PDF file from HTML-string.

    :param string_html: HTML-string
    :param base_url: base url address, to find out path to statics
    :return: object `weasyprint.HTML`
    """
    return HTML(string=string_html, encoding="utf-8", base_url=base_url)


def content_template__render_html(
    *, content_template: ContentTemplate, template_context: dict
) -> str:
    return content_template.render(template_context)


def content_template__render_pdf(
    *, content_template: ContentTemplate, template_context: dict
) -> bytes:
    """
    Render of print form in pdf-format
    """
    html_string = content_template__render_html(
        content_template=content_template, template_context=template_context
    )
    return content_template__create_pdf_from_html_str(
        string_html=html_string
    ).write_pdf()


def content_template__by_uuid(*, template_uuid: uuid.UUID) -> ContentTemplate:
    content_template = content_template__find_by_uuid(
        content_template_uuid=template_uuid
    )

    if not content_template:
        raise ContentTemplateNotFound(content_template_uuid=template_uuid)

    return content_template
