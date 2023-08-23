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

Run the following command from project root to setup the FCE records in MongoDB database: 

```commandline
python -c "from fce_bot.db.fce_data_transform import transform_main; transform_main()"
```

Run the following command to flush and setup the user query records collection (**Do not use the production since it 
will wipe out all data**): 

```commandline
python -c "from fce_bot.db.create_query_records_collection import create_query_records_collection; create_query_records_collection()"
```