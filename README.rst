===============================
DRLS
===============================

Zhejiang University software college dormitory random lottery system

需求介绍
--------
1.可配置学生的抽签的权重，通过Excel上传学生名单以及权重。

2.要求随机抽签的结果可复现。

项目介绍
--------
此项目为浙江大学软件学院的宿舍随机抽签系统，采用**随机区间算法**，权重即为改学生的随机区间大小，同时为实现随机结果可复现的需求，采用初始化随机种子的方法，需要强调的是**初始化随机种子以及学生名单顺序均由辅导员当天确定**，且经过**学生同意**，不存在提前确定的学生区间以及随机种子的情况，保证**抽检的公平**。

如有问题欢迎提**issue**，若有同学更好的算法实现，欢迎提**pr**以及**star**。



开始使用
---------

项目目录 ``drls/data``，将作为数据存储目录存在，在其中将会生成如下文件:

1. ``lock.txt`` 密码文件，该文件用于控制单次上传excel，并简单验证权限
2. ``num.txt`` 记录需要抽签的目标人数
3. ``random_seed.txt`` 记录当前抽签的随机种子
4. ``studata.xls`` 存储用户信息，仅仅支持xls格式文件，该文件应该只有两个字段，字段1为学号，字段2为抽签权重

请注意，代码执行逻辑为:

如果``lock.txt``存在，则只能够上传一次xls文件，并且需要输入密码，今后访问本程序则只能够验证结果。
    - 如果``lock.txt``存在,``studata.xls``不存在，则允许第一次上传，并要求输入密码
    - 如果``lock.txt``存在,``studata.xls``也存在，不再允许上传，只能够验证上一次随机抽取结果
如果``lock.txt``不存在，则可以多次上传xls数据，并覆盖上一次数据

其他文件如``num.txt``、``random_seed.txt``、``studata.xls``则会自动创建

开始开发
----------


.. code-block:: bash


运行如下的命令将帮助你快速开始 ::

    git clone https://github.com/zju-cst/DRLS
    cd drls
    pip install -r requirements/dev.txt
    npm install
    npm start  # run the webpack dev server and flask server using concurrently

你就可以看到程序在 http://localhost:5000 运行.

如果你不用npm 进行开发的话，那么请在开发之前，在cli中运行如下命令,以设置开发环境变量::

    export FLASK_APP=autoapp.py
    export FLASK_DEBUG=1


部署
----------

部署应用::

    export FLASK_DEBUG=0
    npm run build   # build assets with webpack
    flask run       # start the flask server

在你的生产环境中，请确保 ``FLASK_DEBUG`` 环境变量已经被设置为``0``,只有这样生产配置``ProdConfig`` 才会被使用.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    flask test

Asset Management
----------------

Files placed inside the ``assets`` directory and its subdirectories
(excluding ``js`` and ``css``) will be copied by webpack's
``file-loader`` into the ``static/build`` directory, with hashes of
their contents appended to their names.  For instance, if you have the
file ``assets/img/favicon.ico``, this will get copied into something
like
``static/build/img/favicon.fec40b1d14528bf9179da3b6b78079ad.ico``.
You can then put this line into your header::

    <link rel="shortcut icon" href="{{asset_url_for('img/favicon.ico') }}">

to refer to it inside your HTML page.  If all of your static files are
managed this way, then their filenames will change whenever their
contents do, and you can ask Flask to tell web browsers that they
should cache all your assets forever by including the following line
in your ``settings.py``::

    SEND_FILE_MAX_AGE_DEFAULT = 31556926  # one year
