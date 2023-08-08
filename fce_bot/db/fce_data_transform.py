import pandas as pd
from fce_bot.main import db, project_root, logger, mongo_client as client
from pymongo import MongoClient
from pymongo.database import Database


class FCEDataTransformer:

    def __init__(self, mongo_db: Database):
        self.db = mongo_db
        self.db.drop_collection("fce_raw")

    def populate_raw_data(self, fce_data_file_path: str):
        """
        Inserts all entries of a CSV into a collection called
        """
        raw_data_collection = self.db["fce_raw"]
        raw_data_collection.drop()  # reset raw data collection
        raw_data_frame = pd.read_csv(fce_data_file_path, index_col=False)
        raw_data_collection.insert_many(raw_data_frame.to_dict("records"))


def transform_main():
    transformer = FCEDataTransformer(db)
    transformer.populate_raw_data(project_root / "database/Section_By_Section_Analysis_.csv")
    logger.info("FCE data ETL completed! Please see preview below: ")
    documents = db["fce_raw"].find().limit(10)
    logger.info("\n".join([str(doc) for doc in documents]))


