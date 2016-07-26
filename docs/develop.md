# 开发相关

## 项目目录结构

-   [docs](../docs)

    文档

-   [pdf_conv](../pdf_conv)

    -   [pdf_conv/web2pdf.js](../pdf_conv/web2pdf.js)

        html 转 pdf 程序

-   [prog](../prog)

    第三方工具，`phantomjs` 放在里面。
    
-   [pdf_tmp](../pdf_tmp)

    转 pdf 时，临时存放 pdf，html。可以清空，注意不要删掉 `.git_keep_dir` ，
    否则 git 里没有这个文件夹。
    
-   [webcv](../webcv)

    整个网站放在这里面，这里面的目录结构参考 flask 文档。
        
    -   [webcv/templates](../webcv/templates)
    
        html 模板，参考 jinja2 文档。
        
        -   [webcv/templates/cv](../webcv/templates/cv)
        
            简历模板，`base_*.html`，是模板的模板。所有简历模板都是扩展 `base_*.html` 模板。
            参考 [webcv/templates/cv/demo3.html](../webcv/templates/cv/demo3.html)
        
    -   [webcv/views](../webcv/views)
    
        view functions
    
    -   [webcv/models](../webcv/models)
    
        model，目前没有这个模块。
        
    -   [webcv/static](../webcv/static)
    
        静态文件，js、css、图片等。
        
        第三方的库，如果有多个文件按目录来组织，
        比如 [webcv/static/jquery](../webcv/static/jquery) 里放 `jquery*.js` 和 jQuery 插件。
        
        第三方的库，如果只有一个文件，直接放在 [webcv/static](../webcv/static) 就行。
        
        项目里自己写的 js、css 等放到 [webcv/static/webcv](../webcv/static/webcv) 里。

-   [misc](../misc)

    杂物

## 开发环境

1.  IDE
    安装 PyCharm，点菜单 File -> Import Settings
    导入配置文件 [misc/pycharm_settings_tz.jar](../misc/pycharm_settings_tz.jar)

2.  Python

    使用 Python3.4，先创建一个 Virtualenv，在 Virtualenv 里安装依赖的包：
    
    `pip install -r requirements.txt`
    
3.  安装 redis，并运行。

4.  启动 celery worker：

    `celery -A webcv.celery worker`

5.  运行

    `python3 run_dev_server.py`
    
    打开 http://127.0.0.1:5000/

## Deploy & Configurations

配置文件有两个：

[config_default.json](../config_default.json) 是默认配置文件。

`config.json` 是要修改的配置文件，里面的东西会覆盖 `config_default.json`。

修改时改 `config.json`，不要改 `config_default.json`。`config.json` 不要放到 git 里，。

如何部署待调研。

参考 <https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04>

## 学习资料

### 后端

-   [flask](http://flask.pocoo.org/) Web 框架

    -   MTV: model, templates, view

    -   书
    
        - Instant Flask Web Development
    
        - Building Web Applications with Flask
        
        - Flask Framework Cookbook

-   [celery](http://www.celeryproject.org/) task queue

    <https://www.fullstackpython.com/task-queues.html>
    
    <http://flask.pocoo.org/docs/0.11/patterns/celery/>
    
    <https://github.com/thrisp/flask-celery-example>
    
-   [SQLAlchemy](http://www.sqlalchemy.org/) 数据库工具

    <http://pythoncentral.io/series/python-sqlalchemy-database-tutorial/>

-   [Virtualenv](https://virtualenv.pypa.io/)

    <https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/>

### 前端

参考文档 <https://developer.mozilla.org/en-US/>

-   HTML/CSS

    <http://learn.shayhowe.com/html-css/>

    <http://learnlayout.com/>

-   JavaScript

    -   书
    
        [JavaScript: The Good Parts](http://bdcampbell.net/javascript/book/javascript_the_good_parts.pdf)
        
        DOM Scripting: Web Design with JavaScript and the Document Object Model
        
    -   概念
    
        -   AJAX
        
        -   DOM

-   框架、函数库

    -   Bootstrap: 界面
    
    -   jQuery: 提供 DOM、AJAX api
    
    -   jQuery UI: 界面
    
    -   underscore: 常用函数库
    
    -   Font Awesome： 图标

### 其他

Web 开发的方方面面 <https://www.fullstackpython.com/>
