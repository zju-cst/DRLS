# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask import current_app as app
from drls.utils import read_excel, cal_range, file_exists,allowed_file,app_dir,load_md,JSONR
from drls.rng import RandomGenerator
from werkzeug.utils import secure_filename
import hashlib

import os
import json
import drls.errcode as ERRCODE

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    # if studata.xls exits, show previous random link
    # if lock.txt exits, hide select excel form
    # 如果 studta.xls文件存在，则显示之前的random连接
    # 如果 lock.txt文件存在，则不显示选取文件表单
    show_previous=file_exists(os.path.join(app.config['UPLOAD_FOLDER'],app.config['STUDATA_FILE_NAME']))
    lock_form = file_exists(os.path.join(app.config['UPLOAD_FOLDER'],app.config['LOCK_FILE_NAME']))
    return render_template('public/home.html', data_exist=show_previous, lock=lock_form)

@blueprint.route('/about/')
def about():
    """About page."""
    mdpath = os.path.join(app_dir(),'markdown','about.md')
    return render_template('public/about.html', mdcontent=load_md(mdpath))


@blueprint.route('/upload/', methods=['POST'])
def upload():
    if request.method == 'POST':
        seed = request.form['randomSeed']
        num = request.form['randomNum']
        app.logger.info(seed)
        app.logger.info(num)
        # check passwd
        lock_file_path = os.path.join(app.config['UPLOAD_FOLDER'],app.config['LOCK_FILE_NAME'])
        lock = file_exists(lock_file_path)
        if lock:
            passwd = request.form['passwd']
            app.logger.info(passwd)
            app.logger.info(lock)
            passwd_file = open(lock_file_path,'r')
            real_passwd = passwd_file.readline().strip()
            passwd_file.close()
            if real_passwd != passwd:
                return JSONR(ERRCODE.UNAUTHORIZED,'password was wrong')
        else:
            pass
        seed_file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['RANDOMSEED_FILE_NAME'])
        num_file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['RANDOMNUM_FILE_NAME'])

        # save random_seed
        seed_file = open(seed_file_path,'w')
        try:
            random_seed = int(seed)
            seed_file.write(str(random_seed))
        except ValueError:
            return JSONR(ERRCODE.FORMAT_ERROR,'random seed format error', seed)
        finally:
            seed_file.close()

        # save random_num
        num_file = open(num_file_path,'w')
        try:
            random_num = int(num)
            num_file.write(str(random_num))

        except ValueError:
            return JSONR(ERRCODE.FORMAT_ERROR,'random num format error', num)
        finally:
            num_file.close()

        # save stu file
        file = request.files['fileUploaded']
        if file and allowed_file(file.filename,app.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            # app.logger.info(filename.split('.',1)[0])
            # target_filename = filename.split('.',1)[0] + '-' + str(hashlib.sha224(filename).hexdigest()) +'.'+ filename.split('.',1)[1]
            # TODO only support xls type file
            target_filename = app.config['STUDATA_FILE_NAME']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], target_filename))
            # return redirect(url_for('public.random',filename=filename))
            return JSONR(ERRCODE.SUCCESS,'success')
        else:
            return JSONR(ERRCODE.INVALID_FILE,'invalid file extension')
    return JSONR(ERRCODE.INVALID_REQUEST,'only support post method')

@blueprint.route('/random/', methods=['GET'])
def random():
    """random page."""
    if file_exists(os.path.join(app.config['UPLOAD_FOLDER'],app.config['STUDATA_FILE_NAME'])):
       return render_template('public/random.html')
    return redirect(url_for('public.home'))


@blueprint.route('/rand/', methods=['POST'])
def rand():
    """rand"""
    xls_file  = os.path.join(app.config['UPLOAD_FOLDER'],app.config['STUDATA_FILE_NAME'])
    # get random seed
    seed_file_path = os.path.join(app.config['UPLOAD_FOLDER'],app.config['RANDOMSEED_FILE_NAME'])
    num_file_path = os.path.join(app.config['UPLOAD_FOLDER'],app.config['RANDOMNUM_FILE_NAME'])

    random_num = 0
    random_seed =0
    if file_exists(seed_file_path):
        seed_file = open(seed_file_path)
        seed = 0
        try:
            seed = seed_file.readline().strip()
            random_seed = int(seed)
        except BaseException:
            return JSONR(ERRCODE.FORMAT_ERROR,'convert random seed failed',seed)
        finally:
            seed_file.close()
    if file_exists(num_file_path):
        num_file = open(num_file_path)
        num = 0
        try:
            num = num_file.readline().strip()
            random_num = int(num)
        except BaseException:
            return JSONR(ERRCODE.FORMAT_ERROR,'convert random num failed',num)
        finally:
            num_file.close()
    # calc random result
    if file_exists(xls_file):
       # rand
       dicts = read_excel(xls_file)
       res = RandomGenerator(random_seed, cal_range(dicts), random_num, dicts)
       studs = res.GenerateResult()
       data = {'allstus': dicts,'studs':studs }
       return JSONR(ERRCODE.SUCCESS,'success',data)
    return JSONR(ERRCODE.UNKNOW,'failed')

