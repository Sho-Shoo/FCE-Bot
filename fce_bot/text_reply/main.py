from werobot.messages.messages import TextMessage
from pymongo.database import Database
import traceback


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
            course_number: int = format_course_number(text)
            result = self.query_course(course_number)
            return result
        else:
            return "无法解析查询"

    def query_course(self, course_number: int) -> str:
        try:
            results = list(self.db.fce_records.find({'cnum': int(course_number)}))
            return str(results)
        except Exception as e:
            self.logger.error(f"Following error happened: {e}")
            tb = traceback.format_exc()
            self.logger.error(tb)


def format_course_number(text: str) -> int:
    text = text.replace('-', '')
    text = text.strip()
    return int(text)


def is_course_number(text: str) -> bool:
    """
    Checks if a string is a valid CMU course number, i.e., 15-213, 15112, etc.
    """
    try:
        course_number = format_course_number(text)
        return len(str(course_number)) <= 5
    except ValueError:
        return False
