from collections import OrderedDict
from fce_bot.main import db, logger


def create_canvas_reminder_users_collection():
    """
    Creates an empty collection in db called `canvas_reminder_users` and create index on `user_id` field
    """
    collection_name = "canvas_reminder_users"
    db.drop_collection(collection_name)
    # create collection
    db.create_collection(collection_name)
    # create validation rules
    settings = [('collMod', collection_name),
                ('validator', {'user_id': {'$type': 'string'},
                               'canvas_api_key': {'$type': 'string'}}),
                ('validationLevel', 'moderate')]
    settings = OrderedDict(settings)
    db.command(settings)

    logger.info("`canvas_reminder_users` collection created with corresponding validations")
