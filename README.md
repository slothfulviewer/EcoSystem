安装

使用pip安装： pip install -Ur requirements.txt创建超级用户


创建超级用户

终端下执行:
python manage.py createsuperuser



创建测试数据

终端下执行:
python manage.py create_testdata




收集静态文件

终端下执行:  
python manage.py collectstatic --noinput
python manage.py compress --force





开始运行：
执行： python manage.py runserver
浏览器打开: http://127.0.0.1:8000/ 就可以看到效果了。



服务器部署
本地安装部署请参考 DjangoBlog部署教程 有详细的部署介绍.
本项目已经支持使用docker来部署，如果你有docker环境那么可以使用docker来部署，具体请参考:docker部署
