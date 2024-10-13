import contextlib
import json
import typing

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import BaseFormSet, ModelForm
from django.http import HttpRequest, HttpResponse
from django.template import TemplateDoesNotExist
from django.template.base import UNKNOWN_SOURCE, Template
from django.template.loader import get_template
from django.template.response import TemplateResponse

from apps.django_printforms.admin.forms import (ContentTemplateAdminForm,
                                                ContentTemplateCreateAdminForm)
from apps.django_printforms.common.custom_types import GenericContext
from apps.django_printforms.logic.interactors import \
    content_template__render_pdf
from apps.django_printforms.models import ContentTemplate


@admin.register(ContentTemplate)
class ContentTemplateAdmin(ModelAdmin):
    list_display = ["id", "uuid", "title", "code"]
    search_fields = ["title", "uuid"]

    form = ContentTemplateAdminForm
    change_form_template = "django_printforms/content_template_change_form.html"

    @staticmethod
    def _get_context(request: HttpRequest) -> dict:
        context = request.POST["sample"]
        return json.loads("".join(context))

    @staticmethod
    def _is_pdf_preview(request: HttpRequest) -> bool:
        return "_preview_pdf" in request.POST

    @staticmethod
    def _get_template_with_file_origin(code: str) -> Template | None:
        """Get template from filesystem."""
        with contextlib.suppress(TemplateDoesNotExist):
            template = typing.cast(Template, get_template(code))

            if template.origin.name != UNKNOWN_SOURCE:
                return template

        return None

    def get_form(
        self,
        request: HttpRequest,
        obj: ContentTemplate | None = None,
        change: bool = False,
        **kwargs: typing.Any,
    ) -> typing.Type[ModelForm]:
        if obj:
            kwargs["form"] = ContentTemplateAdminForm
        else:
            kwargs["form"] = ContentTemplateCreateAdminForm
        return super().get_form(request, obj, **kwargs)

    def render_change_form(
        self,
        request: HttpRequest,
        context: GenericContext,
        add: bool = False,
        change: bool = False,
        form_url: str = "",
        obj: ContentTemplate | None = None,
    ) -> TemplateResponse:
        db_template_exists = change
        template_file_exists = False

        if change and obj and obj.code:
            template_file_exists = (
                self._get_template_with_file_origin(obj.code) is not None
            )

        context["db_template_exists"] = db_template_exists
        context["template_file_exists"] = template_file_exists

        return super().render_change_form(request, context, add, change, form_url, obj)

    def response_change(
        self, request: HttpRequest, content_template: ContentTemplate
    ) -> HttpResponse:
        if self._is_pdf_preview(request):
            template_context = self._get_context(request)
            pdf_content = content_template__render_pdf(
                content_template=content_template, template_context=template_context
            )
            response = HttpResponse(pdf_content, content_type="application/pdf")
            response["Content-Disposition"] = 'filename="preview.pdf"'
            return response
        return super().response_change(request, content_template)

    def save_model(
        self, request: HttpRequest, obj: ContentTemplate, form: ModelForm, change: bool
    ) -> None:
        if self._is_pdf_preview(request):
            return None

        return super().save_model(request, obj, form, change)

    def save_related(
        self,
        request: HttpRequest,
        form: ModelForm,
        formsets: typing.Iterable[BaseFormSet],
        change: bool,
    ) -> None:
        if self._is_pdf_preview(request):
            return None

        return super().save_related(request, form, formsets, change)
