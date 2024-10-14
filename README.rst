============
django-printforms
============

django-polls is a Django app to create pdf print forms based on Django Template layout system.

Quick start
-----------

1. Add "printforms" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "printforms",
    ]

2. Run ``python manage.py migrate`` to create the models.

3. Start the development server and visit the admin to create printforms templates.
For example, create template with this html::

    <h1>{{ variable }}</h1>

4. Use it in your project like that::

    from django_printforms.logic.interactors import content_template__render_pdf

    pdf_bytes = content_template__render_pdf(
                    content_template=you-template-object, template_context={'variable': 'hello world'}
                )
