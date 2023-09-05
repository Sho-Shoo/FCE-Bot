import pytest
from fce_bot.canvas_reminder.canvas_reminder import CanvasReminder
from fce_bot.db.init_db import init_db
from fce_bot.main import db, logger, wechat_client
from concurrent.futures import ThreadPoolExecutor

thread_exec = ThreadPoolExecutor(max_workers=8)
API_KEY = "7752~F857Z1znbTlmy1zh0gWJHAwXTCcbNeQPVCtU2aGbTNDGOniwrSVc461CETNNNwe7"


@pytest.mark.asyncio
async def test_load_api_key():
    init_db()
    reminder = CanvasReminder(db, wechat_client, thread_exec, logger)
    result_message = await reminder.load_api_key("fromUser", API_KEY)
    assert "验证成功" in result_message

    results = list(db.canvas_reminder_users.find())
    assert len(results) == 1
    result = db.canvas_reminder_users.find_one({'user_id': 'fromUser'})
    assert result['user_id'] == 'fromUser'
    assert result['canvas_api_key'] == API_KEY


@pytest.mark.asyncio
async def test_load_api_key_failure():
    await test_load_api_key()
    reminder = CanvasReminder(db, wechat_client, thread_exec, logger)
    result_message = await reminder.load_api_key("fromUser", "wrong_key")
    assert "验证失败" in result_message


@pytest.mark.asyncio
async def test_api_key_retrieval():
    await test_load_api_key()
    reminder = CanvasReminder(db, wechat_client, thread_exec, logger)
    retrieved_api_key = await reminder.retrieve_api_key("fromUser")
    assert retrieved_api_key == API_KEY


@pytest.mark.asyncio
async def test_api_key_retrieval_failure():
    await test_load_api_key()
    reminder = CanvasReminder(db, wechat_client, thread_exec, logger)
    try:
        retrieved_api_key = await reminder.retrieve_api_key("stranger")
        assert False, "Should trigger LookupError when looking for API key of non-existent user"
    except LookupError:
        assert True

