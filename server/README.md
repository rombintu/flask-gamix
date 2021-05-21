# FLASK AUTH TEST

## RUN
```
git clone https://github.com/rombintu/flask-auth.git
cd flask-auth
python3 -m venv venv
pip install -r requirements.txt
python
>>> from project import db, create_app
>>> db.create_all(app=create_app())
>>> exit
flask run
```