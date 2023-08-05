## Setup test server locally 

You can start a local development server using command `gunicorn -b 0.0.0.0:8080 fce_bot.main:server`. 

## Running project with Docker

The most recommended way of running the project locally. 

To build image locally: 

```commandline
docker build -t fce-bot .
```

To compose and run the image: 

```commandline
docker-compose up -d 
```