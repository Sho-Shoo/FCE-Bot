from fce_bot.main import logger
from fce_bot.canvas_reminder.canvas_scraper import CanvasScraper
from datetime import datetime
from canvasapi.assignment import Assignment
from canvasapi.course import Course
from pytz import timezone
from concurrent.futures import ThreadPoolExecutor
import pytest

API_URL = "https://canvas.cmu.edu/"
API_KEY = "7752~F857Z1znbTlmy1zh0gWJHAwXTCcbNeQPVCtU2aGbTNDGOniwrSVc461CETNNNwe7"

thread_exec = ThreadPoolExecutor(max_workers=8)
scraper = CanvasScraper(logger, thread_exec)
est = timezone("US/Eastern")
after_time = datetime(2022, 1, 1, 12, 0, 0, 0, tzinfo=est)
before_time = datetime(2023, 1, 1, 12, 0, 0, 0, tzinfo=est)



@pytest.mark.asyncio
async def test_get_future_assignments():
    courses_assignments = await scraper.get_future_assignments(API_KEY, before=before_time, after=after_time)
    courses, assignments = [c_a[0] for c_a in courses_assignments], [c_a[1] for c_a in courses_assignments]
    assert len(assignments) > 0
    assert len(courses) > 0
    assert isinstance(assignments[0], Assignment)
    assert isinstance(courses[0], Course)
