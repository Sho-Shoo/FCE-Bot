from fce_bot.main import logger
from fce_bot.text_reply.canvas_scraper import CanvasScraper
from datetime import datetime
from canvasapi.assignment import Assignment
from canvasapi.course import Course
from pytz import timezone

API_URL = "https://canvas.cmu.edu/"
API_KEY = "7752~F857Z1znbTlmy1zh0gWJHAwXTCcbNeQPVCtU2aGbTNDGOniwrSVc461CETNNNwe7"

scraper = CanvasScraper(logger)
est = timezone("US/Eastern")
after_time = datetime(2022, 1, 1, 12, 0, 0, 0, tzinfo=est)


def test_get_future_assignments():
    courses_assignments = scraper.get_future_assignments(API_KEY, after=after_time)
    courses, assignments = [c_a[0] for c_a in courses_assignments], [c_a[1] for c_a in courses_assignments]
    assert len(assignments) > 0
    assert len(courses) > 0
    assert isinstance(assignments[0], Assignment)
    assert isinstance(courses[0], Course)
