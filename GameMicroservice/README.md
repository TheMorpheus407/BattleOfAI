# Battle of AI Game Microservice

### Visit battleofai.net for more info

##### German Let's Code for the whole project: https://www.youtube.com/user/TheMorpheus407

### Installation

##### Environment variables

|      Key      |      Value      |  DEFAULT  |
|:-------------:|:---------------:|:---------:|
| DB_HOSTNAME   | MySQL hostname  | localhost |
| DB_PORT       | MySQL port      | 3306      |
| DB_USERNAME   | MySQL username  | boai      |
| DB_PASSWORD   | MySQL password  |           |
| DB_DATABASE   | MySQL database  | boai      |

##### Easiest: Run wih docker
```sh
$ docker build -t boaigames .
$ docker run -p 1337:80 \
             -e DP_PASSWORD=MySecretPassword \ 
             boaigames
```
Then the service is running at
```
0.0.0.0:1337/api/
```

Docker Compose:
```
version: '3'
services:
  boaiiam:
    image: boaiiam
    restart: always
    environment:
      DB_HOSTNAME: localhost
      DB_PORT: 3306
      DB_USERNAME: boai
      DB_PASSWORD: PASSWORD
      DB_DATABASE: boai
```

##### For Devs (and hardcore people): Run locally
Install the dependencies and start the server. If not installed: Install python 3 and pip first!

```sh
$ pip install -r requirements.txt
$ PYTHONPATH="${PYTHONPATH}:/app:/app/GameMicroservice"
$ export DB_PASSWORD=MyDBPassword
$ export PYTHONPATH
$ python app.py
```


### Todos

 - Moar Tests! srsly, have to do this.
 - Moar Games = More Fun


**Free Software, Hell Yeah!**


   [Python 3]: <https://www.python.org/>
   [Python Flask]: <http://flask.pocoo.org/>
   [Flask Restplus]: <https://github.com/noirbizarre/flask-restplus>
   [SQLAlchemy]: <https://www.sqlalchemy.org/>
