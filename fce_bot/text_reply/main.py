from werobot.messages.messages import TextMessage
from pymongo.database import Database


class TextMessageReplier:
    """
    Main class for handling textual messages. Currently have the following functionalities:
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

    def __init__(self, db: Database, logger):
        self.db = db
        self.logger = logger

    def reply(self, message):
        text = message.content
        if is_course_number(text):
            course_number = format_course_number(text)
            result = self.query_course(course_number)
            return result
        else:
            return "无法解析查询"

    def query_course(self, course_number: str) -> str:
        results = list(self.db.fce_records.find({'cnum': course_number}))
        return str(results)


def format_course_number(text: str) -> str:
    text = text.replace('-', '')
    text = text.strip()
    return text


def is_course_number(text: str) -> bool:
    """
    Checks if a string is a valid CMU course number, i.e., 15-213, 15112, etc.
    """
    text = format_course_number(text)
    return text.isdigit() and len(text) <= 5
