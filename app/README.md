# P8-nutella
## Class project : Create a platform for nutella lovers.

### OpenClassrooms - DA Python - v1.

This project was developped with Python 3.10.2

In order to run this repo locally :

Clone the repo on your local machine.
```
git clone https://github.com/SLB974/P8-nutella.git
```

Create and activate a virtual environment.
```
python -m venv <env name> --prompt nutella
<env name>/scripts/activate
```

Install requirements with pip.
```
python -m pip install -r requirements.txt
```

Apply migrations
```
python manage.py migrate
```

Populate database
```
python manage.py fetchdata
```

Run test by using coverage.
```
coverage run manage.py test -v 2
coverage html
```

Run local server and enjoy !
```
python manage.py runserver
```

You can find this project in production at https://pur-beurre-974.herokuapp.com
