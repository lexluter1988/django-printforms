from __future__ import annotations

import typing

from django.core.exceptions import MultipleObjectsReturned
from django.template import Template, TemplateDoesNotExist
from django.template.loaders.base import Loader as BaseLoader

from django_printforms.logic.selectors import content_template__find_by_code
from django_printforms.models import ContentTemplate

if typing.TYPE_CHECKING:
    from django.template import Origin


class ContentTemplateDBLoader(BaseLoader):
    def get_template(
        self, template_name: str, skip: list[Origin] | None = None
    ) -> Template:
        try:
            template = content_template__find_by_code(code=template_name)
            return Template(template.content)
        except (MultipleObjectsReturned, ContentTemplate.DoesNotExist):
            raise TemplateDoesNotExist(template_name)
