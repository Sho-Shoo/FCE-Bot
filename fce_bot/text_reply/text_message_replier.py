from werobot.messages.messages import TextMessage
from pymongo.database import Database
from fce_bot.text_reply.dining_scraper import DiningScraper
import traceback


class TextMessageReplier:
    """
    Main class for handling textual messages. Currently have the following functionalities:
        1. Reply to course number query
        2. Reply to CMU dining location query (planned)
        3. Reply to CMU library available space query (planned)
    """

    def __init__(self, db: Database, logger):
        """
        Initialize a TextMessageReplier instance.
        Parameters:
            db: PyMongo Database instance
            logger: logger for printing information and trace
        """
        self.db = db
        self.logger = logger
        self.dining_scraper = DiningScraper(logger)

    def reply(self, message):
        """
        Reply to a text message
        Parameters:
            message (TextMessage): User input message
        Returns:
            str: Reply string
        """
        text: str = message.content
        if is_course_number(text):
            course_number: str = format_course_number(text)
            result = self.query_course(course_number)
            return result
        elif dining_location_reply := self.dining_scraper.query_dining_location(text):
            return dining_location_reply
        else:
            return "无法解析查询"

    def query_course(self, course_number: str) -> str:
        try:
            reply = ""
            result_documents = self.db.fce_records.aggregate([
                {'$match': {'cnum': course_number}},
                {'$addFields': {'offering_length': { "$size": "$offerings" }}},
                {'$sort': {
                    'offering_length': -1,
                    'instructor': 1
                }},
                {'$limit': 5}
            ])

            for document in result_documents:
                reply += format_document(document)

            return reply if reply != "" else "未找到对应课程"
        except Exception as e:
            self.logger.error(f"Following error happened: {e}")
            tb = traceback.format_exc()
            self.logger.error(tb)
            return "出现错误"


def format_course_number(text: str) -> str:
    text = text.replace('-', '')
    text = text.replace(' ', '')
    text = text.strip()
    return text


def is_course_number(text: str) -> bool:
    """
    Checks if a string is a valid CMU course number, i.e., 15-213, 15112, etc.
    """
    course_number = format_course_number(text)
    return course_number.isdigit() and len(course_number) <= 5


def format_document(document: dict) -> str:
    """
    Format a Mongo document, as python dict, into string
    """
    hour, rating, instructor = document["avg_hours"], document["avg_rating"], document["instructor"]
    course_number = document["cnum"]
    offerings = ", ".join(sorted(document["offerings"]))
    formatted = f"课号: {course_number}\n" \
                f"教授: {instructor}\n" \
                f"评分: {round(rating, 2)}\n" \
                f"小时数: {round(hour, 2)}\n" \
                f"以往任教: {offerings}\n\n"
    return formatted
