# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
import xlrd

def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)

def read_excel(path):
    student = {}
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrow = table.nrows
    for i in range(nrow):
        key = table.cell_value(i,0)
        value = table.cell_value(i,1)
        student[key] = value
    return student

