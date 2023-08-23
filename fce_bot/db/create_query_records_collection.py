from collections import OrderedDict
from fce_bot.main import db, logger


def create_query_records_collection():
    """
    Creates an empty collection in db called `query_records` and create index on `user_id` field
    """
    collection_name = "query_records"
    db.drop_collection(collection_name)
    # create collection
    db.create_collection(collection_name)
    # create validation rules
    settings = [('collMod', collection_name),
                ('validator', {'user_id': {'$type': 'string'},
                               'query': {'$type': 'string'},
                               'time': {'$type': 'int'}}),
                ('validationLevel', 'moderate')]
    settings = OrderedDict(settings)
    db.command(settings)

    logger.info("`query_records` collection created with corresponding validations")
