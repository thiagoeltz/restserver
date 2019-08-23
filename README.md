# Server Rest Example with JWT
## Python

* Test Project made by back-end developer

* Created web application with endpoints.

* Database used was redis, to storage users-mail, password and token.

* Test Coverage 91% 

* Version: github

* Application supports windows and linux

* Used lib(gunicorn) to use wsgi application.

* To deploy this application need to create a redis database

* Redis database is in a zip file in this repository, just unzip and start `redis-server` as administrator in `c:\redis`

* Put the application on Kibana Elastic Search and Google Auth


## Commands Local:

================= User Genarate Token =================
```
curl -X POST \
  http://localhost:5000/registration \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "your mail",
    "password": "your password"
}'
```
========================Current========================
```
curl -X GET \
  http://127.0.0.1:5000/current \
  -H 'Authorization: Bearer your token' \
  -H 'Content-Type: application/json' \
```
========================Next============================
```
curl -X GET \
  http://127.0.0.1:5000/next \
   -H 'Authorization: Bearer your token' \
   -H 'Content-Type: application/json' 
```
=======================New Current======================
```
curl -X PUT \
  http://127.0.0.1:5000/current \
  -H 'Authorization: Bearer your token' \
  -H 'Content-Type: application/json' \
  -d '{"current": 1155}'
```
========================Refresh Token ==================
* Remember if you refresh your token, the access token will change for a new one
```
curl -X POST \
  http://localhost:5000/refresh \
  -H 'Authorization: Bearer your refresh token' \
  -H 'Content-Type: application/json'
```
=======================Retrieve Token ==================
```
curl -X POST \
  http://localhost:5000/retrieve \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "your user e-mail",
    "password": "your password"
}'
```


