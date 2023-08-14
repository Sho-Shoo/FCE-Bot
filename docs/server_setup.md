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

## Setup of MongoDB 

Run the following command from project root to setup the MongoDB database: 

```commandline
python -c "from fce_bot.db.fce_data_transform import transform_main; transform_main()"
```