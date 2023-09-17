import traceback
from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.assignment import Assignment
from canvasapi.paginated_list import PaginatedList
from canvasapi.user import User
from datetime import datetime
from pytz import timezone
from concurrent.futures import ThreadPoolExecutor


class CanvasScraper(object):

    def __init__(self, logger, thread_exec: ThreadPoolExecutor):
        self.url = "https://canvas.cmu.edu/"
        self.logger = logger
        self.thread_exec = thread_exec

    async def get_future_assignments(self, api_key: str, after: datetime = None) -> list[tuple[Course, Assignment]]:
        """
        Get a list of future assignments (after certain datetime, default to be now), tupled with corresponding Course
        objects
        """
        if not after:
            est = timezone("US/Eastern")
            after = datetime.now(est)

        try:
            user = Canvas(self.url, api_key).get_current_user()
            courses = self._get_courses(api_key)
            futures = []
            for course in courses:
                future = self.thread_exec.submit(self._get_assignments_of_user_and_course, user, course, after)
                futures.append(future)
            for i in range(len(futures)):
                futures[i] = futures[i].result()

            courses_assignments: list[tuple[Course, Assignment]] = []
            for future in futures:
                for course_assignment in future:
                    courses_assignments.append(course_assignment)

            return courses_assignments
        except Exception as e:
            self.logger.error(f"Following error happened: {e}")
            tb = traceback.format_exc()
            self.logger.error(tb)

    def _get_courses(self, api_key: str) -> list[Course]:
        """
        Get the list of valid course (with course code) from the current user providing the API key
        """
        courses = Canvas(self.url, api_key).get_current_user().get_courses()
        valid_courses = [course for course in courses if hasattr(course, 'course_code')]
        return valid_courses

    @staticmethod
    def _get_assignments_of_user_and_course(user: User, course: Course,
                                            after: datetime) -> list[tuple[Course, Assignment]]:
        """
        Get the future assignments after a certain datetime (tupled with Course objects) of a user-course pair
        """
        est = timezone("US/Eastern")
        assignments: PaginatedList = user.get_assignments(course)
        future_assignments = [a for a in assignments if a.due_at and
                              datetime.strptime(a.due_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=est) > after]  # TODO: change timezone to UTC
        result = [(course, a) for a in future_assignments]
        return result

