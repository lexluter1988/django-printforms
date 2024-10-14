from __future__ import annotations

from django.db import models
from django.template import Context, Template, TemplateSyntaxError

from django_printforms.common.custom_types import GenericContext
from django_printforms.common.models import DefaultModel


def help_message_default() -> dict:
    return {"variable_name": "variable_value"}


class ContentTemplate(DefaultModel):
    class SensitiveData:
        include: list[str] = []
        exclude = ["title", "code", "content", "help_message"]

    title = models.CharField("template name", max_length=255)
    code = models.CharField(
        "template code",
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text='example: "content_templates/base.html"',
    )  # null_by_design
    content = models.TextField(
        "template text",
    )

    help_message = models.JSONField(
        "dictionary example",
        default=help_message_default,
        blank=True,
        null=True,
        help_text="variable dictionary example in json",
    )  # null_by_design

    def __str__(self) -> str:
        return self.title

    def render(self, context: GenericContext) -> str:
        template = Template(self.content)
        try:
            return template.render(Context(context))
        except TemplateSyntaxError:
            return ""
