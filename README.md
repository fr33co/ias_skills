# Steps to init dockerized project

1. Create the virtual environment

```bash
$ mkdir project
$ cd project
$ python3 -m venv venv
```

2. Activate the virtual environment

```bash
$ source venv/bin/activate
```

3. Get the code

```bash
$ git clone git@github.com:fr33co/ias_skills.git
```

4. Move to the files project

```
$ cd ias_skils
```

5. Build the image: docker build -t flasktest:1.0 .

6. Run the docker container: docker run -d -p 8085:8085 flasktest:1.0

```docker
$ docker container ls
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                                       NAMES
e4766e5d8a48   flasktest:1.0   "python src/app.py -…"   47 seconds ago   Up 46 seconds   0.0.0.0:8085->8085/tcp, :::8085->8085/tcp   upbeat_pare
```

7. Follow the logs: docker logs --follow container_id

```docker
$ docker logs --follow e4766e5d8a48
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8085
 * Running on http://172.17.0.2:8085
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 122-710-920
172.17.0.1 - - [13/Apr/2024 18:24:08] "GET / HTTP/1.1" 404 -
172.17.0.1 - - [13/Apr/2024 18:24:08] "GET /favicon.ico HTTP/1.1" 404 -
172.17.0.1 - - [13/Apr/2024 18:24:15] "GET /airline HTTP/1.1" 308 -
172.17.0.1 - - [13/Apr/2024 18:24:15] "GET /airline/ HTTP/1.1" 200 -
172.17.0.1 - - [13/Apr/2024 18:30:57] "GET /airline/users HTTP/1.1" 200 -
172.17.0.1 - - [13/Apr/2024 18:31:06] "GET /airline/users/create HTTP/1.1" 200 -
172.17.0.1 - - [13/Apr/2024 18:31:32] "GET /airline/users HTTP/1.1" 200 -
172.17.0.1 - - [13/Apr/2024 18:35:03] "POST /airline/users/create/ HTTP/1.1" 404 -
172.17.0.1 - - [13/Apr/2024 18:35:07] "POST /airline/users/create HTTP/1.1" 200 -
172.17.0.1 - - [13/Apr/2024 18:36:27] "GET /airline/users HTTP/1.1" 200 -
```

# API's Endpoints

1. Root endpoint (GET)

http://localhost:8085/airline/

* Returns

```json
{
  "msg": "Welcome"
}
```

2. Create users (POST)

http://localhost:8085/airline/users/create

* Body

```json
{
  "username": "Test1",
  "email": "test1@test1.com"
}
```

* Returns

```
{
  "email": "test1@test1.com",
  "id": 1,
  "username": "Test1"
}
```

3. Get all users (GET)

http://localhost:8085/airline/users

* Returns

```
[
  {
    "email": "test1@test1.com",
    "id": 1,
    "username": "Test1"
  }
]
```