# Candy(TODO)
## 本地运行
```shell
virtualenv venv
source venv/bin/activate
pip3 install -i https://pypi.doubanio.com/simple -U pip
pip3 install -i https://pypi.doubanio.com/simple -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
# 开发环境默认会找.env文件
python3 manage.py runserver
# 生产环境启动时手动指定读取哪个env文件(env.prod)
ENV_PATH=.env.prod python3 manage.py runserver
```