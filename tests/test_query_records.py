from test_configs import tester, make_xml
from fce_bot.main import db
from fce_bot.db.create_query_records_collection import create_query_records_collection
import pytest


@pytest.fixture()
def database():
    # setup
    db.drop_collection("query_records")
    create_query_records_collection()

    yield db

    # teardown
    db.drop_collection("query_records")
    create_query_records_collection()


def test_query_record(database):
    reply = tester.send_xml(make_xml("36200"))._args['content']
    assert "36200" in reply
    assert "课号" in reply
    assert "评分" in reply

    # send more queries
    tester.send_xml(make_xml("15150"))
    tester.send_xml(make_xml("21127"))
    tester.send_xml(make_xml("00000"))  # this should not be recorded

    query_records = list(database.query_records.find())
    assert len(query_records) == 3
    assert query_records[0]["user_id"] == "fromUser"
    assert query_records[0]["query"] == "36200"
    assert query_records[1]["query"] == "15150"
    assert query_records[2]["query"] == "21127"

