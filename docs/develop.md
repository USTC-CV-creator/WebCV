# 开发相关

## 项目目录结构

-   [docs](../docs)

    文档

-   [pdf_conv](../pdf_conv)

    [pdf_conv/web2pdf.js](../pdf_conv/web2pdf.js)

    html 转 pdf 程序

-   [prog](../prog)

    第三方工具，`phantomjs` 放在里面。
    
-   [pdf_tmp](../pdf_tmp)

    转 pdf 时，临时存放 pdf，html。可以清空，注意不要删掉 `.git_keep_dir` ，
    否则 git 里没有这个文件夹。
    
-   [webcv](../webcv)

    整个网站放在这里面，这里面的目录结构参考 flask 文档。
        
    -   [webcv/templates](../webcv/templates)
    
        html 模板
        
    -   [webcv/templates/cv](../webcv/templates/cv)
    
        简历模板
        
    -   [webcv/views](../webcv/views)
    
        view functions
    
    -   [webcv/models](../webcv/models)
    
        model，目前没有这个模块。
        
    -   [webcv/static](../webcv/static)
    
        静态文件，js、css、图片等。
        
        第三方的库，如果有多个文件按目录来组织，
        比如 [webcv/static/jquery](../[webcv/static/jquery) 里放 `jquery*.js` 和 jQuery 插件。
        
        第三方的库，如果只有一个文件，直接放在 [webcv/static](../webcv/static) 就行。
        
        项目里自己写的 js、css 等放到 [webcv/static/webcv](../webcv/static/webcv) 里。
