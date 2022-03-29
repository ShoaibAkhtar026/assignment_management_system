# Assignment Management System

##Install Dependencies

### 1- Install python related dependencies

```
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.9
sudo apt-get install python3-pip python3-dev python3.9-venv
```

## Setup Virtual Environment
Create virtual env using following command
```
python3.9 -m venv venv
```

Activate environment using following command
```
source venv/bin/activate
```

## Install requirements

Install requirements using following command
```
pip3 install -r requirements.txt
```
##Create and run migrations
Run following command to create django migrations
```
python manage.py makemigrations
```
Run following command to apply django migrations in database
```
python manage.py migrate
```

## Run API Server
```
python3 manage.py runserver
```

API Server will be running on http://127.0.0.1:8000
