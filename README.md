# Candy - 基于Django3.2 + Vue3 + MySQL8 可进行二次开发的Admin脚手架

权限控制基于RBAC，前端权限控制精确到菜单和按钮级别。

## 本地开发环境搭建
```shell
virtualenv venv
source venv/bin/activate
pip3 install -i https://pypi.doubanio.com/simple -U pip
pip3 install -i https://pypi.doubanio.com/simple -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
# 开发环境默认会找项目根目录下的.env环境变量文件
python3 manage.py runserver
# 前端开发环境搭建见前端仓库 https://github.com/hashqueue/candy-web.git
#####################################################
###               Done!下边的命令了解即可            ###
#####################################################
# 生产环境使用开发服务器启动时手动指定读取哪个env文件(项目根目录下的.env.prod)
ENV_PATH=.env.prod python3 manage.py runserver
# Django导出数据库数据
python3 manage.py dumpdata --format json --indent 2 -o init_db.json
# Django导入已有的数据到新的数据库中
python3 manage.py loaddata init_db.json
# 开发环境下使用daphne启动项目
daphne -b 0.0.0.0 -p 8000 candy.asgi:application
# 生产环境下使用daphne启动项目
ENV_PATH=.env.prod daphne -b 0.0.0.0 -p 8000 candy.asgi:application
```

## 生产环境部署

1. 安装docker和docker-compose和git
    * [docker安装步骤(官方文档)](https://docs.docker.com/engine/install/)
    * [docker-compose安装步骤(官方文档)](https://docs.docker.com/compose/install/)
    * [git安装步骤(官方文档)](https://git-scm.com/download/linux)
2. git拉取本项目代码到服务器
    ```shell
    # 下载后端源码
    git clone https://github.com/hashqueue/candy.git
    cd candy
    # 下载前端源码
    git clone https://github.com/hashqueue/candy-web.git
    cd .. # 回到后端代码目录
    ```
3. docker-compose启动项目(前端，后端，数据库)
    ```shell
    # 部署并启动项目
    docker-compose --env-file=./.env.prod up -d
    # 容器全部启动成功后，手动进入backend容器，初始化数据库数据(此步骤仅第一次部署项目时需要操作！！！)。
    docker exec -it backend /bin/bash # 进入backend容器
    ENV_PATH=.env.prod python3 manage.py loaddata init_db.json # 初始化数据库数据
    ```
项目部署成功后访问`http://服务器域名或IP/`即可跳转到登录页面

登录页
![登录页](images/login.png)

系统首页
![系统首页](images/index.png)

权限管理
![权限管理](images/permission.png)

角色管理
![角色管理](images/role.png)

用户管理
![用户管理](images/user.png)

部门管理
![部门管理](images/dept.png)

服务器性能监控
![服务器性能监控](images/server.png)

个人中心
![个人中心](images/profile.png)

swagger格式接口文档`http://服务器域名或IP/api/v1/swagger/`
![swagger格式接口文档](images/swagger.png)

redoc格式接口文档`http://服务器域名或IP/api/v1/redoc/`
![redoc格式接口文档](images/redoc.png)

