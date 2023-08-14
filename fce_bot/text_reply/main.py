from werobot.messages.messages import TextMessage
from pymongo.database import Database


def text_reply_main(message: TextMessage, db: Database, logger) -> str:
    """
    Main function for reply to textual messages. Currently have the following functionalities:
        1. Reply to course number query
        2. Reply to CMU dining location query (planned)
        3. Reply to CMU library available space query (planned)
    Parameters:
        message (TextMessage): User input message
        db: PyMongo Database instance
        logger: logger for printing information and trace
    Returns:
        str: Reply string
    """

    text = message.content
    return f"你说了：{text}"
