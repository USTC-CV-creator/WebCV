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
        
            简历模板，`base_*.html`，是模板的模板。
        
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

## Deploy & Configurations

TBA

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
