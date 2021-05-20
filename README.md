# pytest-monitor-backend

## Installation

### Put MongoDB credentials to ./env/mongo.env

#### Example: 

```
MONGO_HOST=pymon_mongo_local
MONGO_PORT=27017
MONGO_INITDB_DATABASE=local_db
MONGO_INITDB_ROOT_PASSWORD=pass
MONGO_INITDB_ROOT_USERNAME=user
```

### Build container

```shell script
docker build -t pymon_backend .
```

### Run container

```shell script
docker-compose up -d
```

## Usage 

### install pytest-monitor

```shell script
pip install pytest-monitor
```

### Run test with pytest-monitor

```shell script
pytest --remote-server http://server_name:5000 test1.py
```

### Get info from MongoDB

```mongojs
use pymon

db.context.find()
db.session.find()
db.metrics.find()
```


## Links

- [pytest-monitor](https://pytest-monitor.readthedocs.io/)
- [flask-restful](https://flask-restful.readthedocs.io/en/latest/quickstart.html)
- [flask-production-recipes](https://www.toptal.com/flask/flask-production-recipes)
- [Flask Rest API -Part:6- Testing REST APIs](https://dev.to/paurakhsharma/flask-rest-api-part-6-testing-rest-apis-4lla)
