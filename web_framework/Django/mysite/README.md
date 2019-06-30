# 1.新建项目 #


命令行新建一个mysite项目

    django-admin startproject mysite

> 给项目命名时，项目名称不能Python和Django的内部组件名称同名。
尤其，你应该避免使用类似django（与Django自身冲突）或测试（与Python内建的包冲突）这样的名称。


结构：
+ mysite/       （项目存放的目录名称，可调整）
   + manage.py      一个命令行工具，可让你以各种方式与该 Django 项目进行交互。
   + mysite     项目的真正的Python包
      + __init__.py
      + settings.py     (该Django 项目的设置/配置)
      + urls.py     (该Django项目的URL声明)
      + wsgi.py     (用于你的项目的与WSGI兼容的Web服务器入口 )

* * *

查看django版本：python -m django --version


模型变更的三个步骤：
1. 修改你的模型（在models.py文件中）。
2. 运行python manage.py makemigrations ，为这些修改创建迁移文件
3. 运行python manage.py migrate ，将这些改变更新到数据库中。


具体的url对应的方法在view.py中定义

使用以下命令创建一个 polls 的 app
    
    django-admin.py startapp polls
    
 
+ polls/
    + __init__.py
    + admin.py  注册模块来增加管理员界面
    + apps.py   app定义
    + migrations/
        + __init__.py
    +models.py  该app的表定义
    + tests.py
    + urls.py   该app的url匹配规则
    + views.py  url对应的视图函数
    

在setting中设置激活的INSTALLED_APPS

相关命令
    
    python manage.py migrate   # 创建表结构migrate查看INSTALLED_APPS设置并根据mysite/settings.py文件中的数据库设置创建任何必要的数据库表
    数据库的迁移还会跟踪应用的变化（我们稍后会讲到）
    python manage.py makemigrations polls  # 让 Django 知道我们在我们的模型有一些变更
    python manage.py migrate polls   # 创建表结构