# flask-restful-boilerplate

## Overview
python flask boilerplate

## Getting Started
### Prerequisites
    * python >= 3.7.2
    * Mysql
    * Pyenv or virtualenv
   
### Installing
Using Pyenv 
```
pyenv install  3.7.2
pyenv virtualenv 3.7.2 [environemt name]
pip install -r requirements.txt
export ENV=config.BaseConfig
python run.py
```

## Running The Tests
Run pytest
```pytest```

## Built With
    * Framework: Flask
    * ORM: SQLAlchemy
    * Validator&Serializer: Marshmallow
    * Test: pytest, pytest-bdd
    
## StyleGuide
- [PEP8](https://www.python.org/dev/peps/pep-0008/) 
- [Google Python style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md) 

## Structure
```
Root
├── project
│   ├── controllers
│   ├── models
│   ├── services
│   ├── utils
├── ├── app.py
├── ├── databases.py
├── config.py
├── conftest.py
└── requirements.txt
```
### controllers
API Endpoint

### models
SQLAlchemy ORM Model

### services
business logic

### utils
utils

## config.py
configs
```
config.BaseConfig : local
config.TestConfig : test
config.ProductionConfig: production
```

### conftest.py
configuration for pytest

### requirements.txt
packages
