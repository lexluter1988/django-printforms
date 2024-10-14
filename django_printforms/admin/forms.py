from __future__ import annotations

from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.template import Context, Template, TemplateSyntaxError
from django_ace import AceWidget

from django_printforms.models import ContentTemplate


class ContentTemplateCreateAdminForm(ModelForm):
    class Meta:
        model = ContentTemplate
        fields = ["title", "code"]


class ContentTemplateAdminForm(ModelForm):
    class Meta:
        model = ContentTemplate
        fields = "__all__"

    sample = forms.JSONField(
        label="Variables editor",
        required=False,
        # widget=JSONEditorWidget(width='90%'),
        initial={"variable_name": "variable_value"},
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["content"].widget = AceWidget(
            mode="html", width="90%", height="500px"
        )

    def clean_content(self) -> str:
        content = self.cleaned_data["content"]
        if content:
            try:
                Template(content).render(Context())
            except TemplateSyntaxError as e:
                raise ValidationError(str(e))
        return content
