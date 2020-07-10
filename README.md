# medhub Python backend
medhub for vendor and flutter api server using python


## 1. Getting Started

### 1.1. Python Flask Server
Run the following commands to start:


```
pip install -r requirements.txt

python app.py
```

### 1.2. Local mongo docker easy setup (optional)
if you have docker setup then simply run the following code:

```
docker run --name mongo -p 27017:27017 --rm -it -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root -v `pwd`/mongo-scripts/:/docker-entrypoint-initdb.d/ mongo mongod --auth
```

This will host a local mongo instance or you can use a remote mongo server


### 1.3. Setting environment variables

create a .env file, that file will have MC and flask debug status

set the following settings for development 
```
MC = "mongodb://root:root@localhost:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false"
DEBUG = True
```