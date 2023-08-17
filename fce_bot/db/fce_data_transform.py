import pandas as pd
from fce_bot.main import db, project_root, logger
from pymongo.database import Database
import datetime

TODAY = datetime.date.today()
YEAR = TODAY.year


class FCEDataTransformer:

    def __init__(self, mongo_db: Database, trace_back: int = 4):
        """
        Stores the DB object within the object
        Parameters:
            mongo_db: PyMongo Database object
            trace_back (int): number of years to trace back
        """
        self.db = mongo_db
        self.trace_back = trace_back

    def populate_raw_data(self, fce_data_file_path: str):
        """
        Inserts all entries of a CSV into a collection called
        """
        raw_data_collection = self.db["fce_raw"]
        raw_data_collection.drop()  # reset raw data collection
        raw_data_frame = pd.read_csv(fce_data_file_path, dtype={'Num': 'string'}, index_col=False)
        raw_data_collection.insert_many(raw_data_frame.to_dict("records"))

    def transform_raw_data(self):
        """
        Transforms the raw FCE data and store the parsed FCE records into a separate collection named fce_records
        """
        fce_records = self.db["fce_records"]
        fce_records.drop()

        self.db.fce_raw.aggregate([
            {'$match': {'Year': {'$gt': YEAR - self.trace_back}}},
            {'$addFields': {'offering': {'$concat': [{'$toString': '$Year'}, ' ', '$Sem']}}},
            {'$group': {
                '_id': {'cnum': '$Num', 'instructor': '$Instructor', 'cname': '$Course Name'},
                'avg_hours': {'$avg': '$Hrs Per Week'},
                'avg_rating': {'$avg': '$Overall course rate'},
                'offerings': {'$addToSet': '$offering'}
            }},
            {'$addFields':
                 {'cnum': '$_id.cnum',
                  'instructor': '$_id.instructor',
                  'cname': '$_id.cname'},
             },
            {'$unset': '_id'},
            {'$merge': {'into': 'fce_records'}}
        ])


def transform_main():
    """
    Main function to populate the database with FCE CSV file.
    """
    transformer = FCEDataTransformer(db)
    transformer.populate_raw_data(project_root / "data/Section_By_Section_Analysis_.csv")
    logger.info("FCE data ETL completed! Please see preview below: ")
    documents = db["fce_raw"].find().limit(10)
    logger.info("\n".join([str(doc) for doc in documents]))

    transformer.transform_raw_data()
    logger.info("Records successfully parsed!")
