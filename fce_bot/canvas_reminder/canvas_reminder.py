import traceback
from concurrent.futures import ThreadPoolExecutor, Future
from pymongo.database import Database
from canvasapi import Canvas
from canvasapi.exceptions import InvalidAccessToken


class CanvasReminder(object):
    """
    CanvasReminder class that 1) loads users' Canvas API key into DB, 2) schedules canvas scraping job every day, 3)
    load reminding jobs into scheduler
    """

    def __init__(self, db: Database, wechat_client, thread_exec: ThreadPoolExecutor, logger):
        self.db = db
        self.logger = logger
        self.we_client = wechat_client
        self.url = "https://canvas.cmu.edu/"
        self.thread_exec = thread_exec

    async def load_api_key(self, user_id: str, canvas_api_key: str) -> str:
        """
        Load valid Canvas API key into DB. Returns a success for failure message
        Arguments:
            user_id (str)
            canvas_api_key (str)
        Returns:
            (str): result message if whether key validation is correct
        """
        if await self._validate_api_key(canvas_api_key):
            self.db.canvas_reminder_users.insert_one({'user_id': user_id,
                                                      'canvas_api_key': canvas_api_key})
            return "API Key验证成功，Canvas作业截止提醒服务将于明日启动"
        else:
            return "API Key验证失败，请检查并重试"

    async def retrieve_api_key(self, user_id: str) -> str:
        """
        Retrieves stored Canvas API key using WeChat User ID
        Arguments:
            user_id (str)
        Returns:
            (str): stored Canvas API Key
        Raises:
            LookupError
        """
        user_document = self.db.canvas_reminder_users.find_one({'user_id': user_id})
        if user_document and user_document.get("canvas_api_key"):
            return user_document.get("canvas_api_key")
        else:
            raise LookupError(f"Canvas API key for user '{user_id}' not found")

    async def _validate_api_key(self, api_key: str) -> bool:
        try:
            canvas = Canvas(self.url, api_key)
            future: Future = self.thread_exec.submit(canvas.get_current_user)
            user = future.result()
            return True
        except InvalidAccessToken as e:
            return False
        except Exception as e:
            self.logger.error(f"Following error happened: {e}")
            tb = traceback.format_exc()
            self.logger.error(tb)
            return False

