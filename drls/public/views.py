# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask import current_app as app
from drls.utils import read_excel, cal_range, file_exists,allowed_file,app_dir,load_md,JSONR
from drls.rng import RandomGenerator
from werkzeug.utils import secure_filename

import os
import drls.errcode as ERRCODE



blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    # if studata.xls exits, show previous random link
    # if lock.txt exits, hide select excel form
    # 如果 studta.xls文件存在，则显示之前的random连接
    # 如果 lock.txt文件存在，则不显示选取文件表单
    show_previous=file_exists(app.config.xls_file_path)
    lock_form = file_exists(app.config.lock_file_path)
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
        lock = file_exists(app.config.lock_file_path)
        if lock:
            passwd = request.form['passwd']
            app.logger.info(passwd)
            app.logger.info(lock)
            app.config.lock_file_lock.acquire()
            passwd_file = open(app.config.lock_file_path,'r')
            try:
                real_passwd = passwd_file.readline().strip()
            finally:
                passwd_file.close()
                app.config.lock_file_lock.release()
            if real_passwd != passwd:
                return JSONR(ERRCODE.UNAUTHORIZED,'password was wrong')

        # save random_seed
        app.config.seed_file_lock.acquire()
        seed_file = open(app.config.seed_file_path,'w')
        try:
            random_seed = int(seed)
            seed_file.write(str(random_seed))
        except ValueError:
            return JSONR(ERRCODE.FORMAT_ERROR,'random seed format error', seed)
        finally:
            seed_file.close()
            app.config.seed_file_lock.release()

        app.config.num_file_lock.acquire()
        # save random_num
        num_file = open(app.config.num_file_path,'w')

        try:
            random_num = int(num)
            num_file.write(str(random_num))

        except ValueError:
            return JSONR(ERRCODE.FORMAT_ERROR,'random num format error', num)
        finally:
            num_file.close()
            app.config.num_file_lock.release()

        # save stu file
        app.config.xls_file_lock.acquire()
        try:
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
        finally:
            app.config.xls_file_lock.release()

    return JSONR(ERRCODE.INVALID_REQUEST,'only support post method')

@blueprint.route('/random/', methods=['GET'])
def random():
    """random page."""
    if file_exists(os.path.join(app.config['UPLOAD_FOLDER'],app.config['STUDATA_FILE_NAME'])):

        random_num = 0
        random_seed =0
        app.config.seed_file_lock.acquire()
        if file_exists(app.config.seed_file_path):
            seed_file = open(app.config.seed_file_path)
            try:
                seed = seed_file.readline().strip()
                random_seed = int(seed)
            except ValueError:
                return render_template('public/random.html',random_seed=0, random_num=0)
            finally:
                seed_file.close()
                app.config.seed_file_lock.release()

        app.config.num_file_lock.acquire()
        if file_exists(app.config.num_file_path):
            num_file = open(app.config.num_file_path)
            try:
                num = num_file.readline().strip()
                random_num = int(num)
            except ValueError:
                return render_template('public/random.html',random_seed=random_seed, random_num=0)
            finally:
                num_file.close()
                app.config.num_file_lock.release()
            return render_template('public/random.html',random_seed=random_seed, random_num=random_num)

    return redirect(url_for('public.home'))


@blueprint.route('/rand/', methods=['POST'])
def rand():
    """rand"""
    # get random seed

    random_num = 0
    random_seed =0
    app.config.seed_file_lock.acquire()
    if file_exists(app.config.seed_file_path):
        seed_file = open(app.config.seed_file_path)
        seed = 0
        try:
            seed = seed_file.readline().strip()
            random_seed = int(seed)
        except BaseException:
            return JSONR(ERRCODE.FORMAT_ERROR,'convert random seed failed',seed)
        finally:
            seed_file.close()
            app.config.seed_file_lock.release()

    app.config.num_file_lock.acquire()
    if file_exists(app.config.num_file_path):
        num_file = open(app.config.num_file_path)
        num = 0
        try:
            num = num_file.readline().strip()
            random_num = int(num)
        except BaseException:
            return JSONR(ERRCODE.FORMAT_ERROR,'convert random num failed',num)
        finally:
            num_file.close()
            app.config.num_file_lock.release()

    # calc random result
    app.config.xls_file_lock.acquire()
    if file_exists(app.config.xls_file_path):
       # rand
       try:
           dicts = read_excel(app.config.xls_file_path)
           res = RandomGenerator(random_seed, cal_range(dicts), random_num, dicts)
           studs = res.GenerateResult()
           res = []
           for key in dicts:
               res.append({"key":key,"value":dicts[key]})
           app.logger.info(res)
           data = {'allstus': res,'studs':studs }

           return JSONR(ERRCODE.SUCCESS,'success',data)
       finally:
            app.config.xls_file_lock.release()
    return JSONR(ERRCODE.UNKNOW,'failed')

