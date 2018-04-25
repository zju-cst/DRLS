# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash, Response
from flask import current_app as app
import markdown2
import os
import xlrd
import json
import collections

def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)

def read_excel(path):
    #有序集合
    student = collections.OrderedDict()
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrow = table.nrows
    for i in range(nrow):
        key = int(table.cell_value(i,0))
        value = table.cell_value(i,1)
        if dict_filter(key):
            student[key] = value
    print(student)
    return student

def cal_range(students):
    sum = 0
    for key in students:
        sum = sum + students[key]
    return sum

def load_md(mdfile_path):
    html= markdown2.markdown_path(mdfile_path)
    return html


def app_dir():
   return os.path.dirname(__file__)


def allowed_file(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extensions

def JSONR(code, msg, data=None):
    return Response(json.dumps({'code': code, 'msg': msg, 'data':data}), mimetype='application/json')

def file_exists(path,isfile=True):
   if os.path.exists(path):
       if isfile and os.path.isfile(path):
           return True
       elif not isfile:
           return True
       else:
           return False
   return False

def dict_filter(item):
    return (str(item).startswith('21751') and len(str(item)) == 8)
