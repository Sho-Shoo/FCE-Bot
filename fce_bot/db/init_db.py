from fce_bot.db.create_query_records_collection import create_query_records_collection
from fce_bot.db.create_canvas_reminder_users_collection import create_canvas_reminder_users_collection


def init_db():
    create_query_records_collection()
    create_canvas_reminder_users_collection()
