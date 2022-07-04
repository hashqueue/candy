# Candy(TODO)
## 本地运行
```shell
virtualenv venv
source venv/bin/activate
pip3 install -i https://pypi.doubanio.com/simple -U pip
pip3 install -i https://pypi.doubanio.com/simple -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```