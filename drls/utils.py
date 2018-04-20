# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
import markdown2


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def load_md(mdfile_path):
    html= markdown2.markdown_path(mdfile_path)
    return html

