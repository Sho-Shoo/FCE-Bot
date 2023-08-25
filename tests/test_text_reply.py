from tests.test_configs import tester, make_xml


def test_course_query():
    reply = tester.send_xml(make_xml("15213"))._args['content']
    assert "15213" in reply
    assert "课号" in reply
    assert "评分" in reply
    print("You can manually check reply below: ")
    print(reply)

    assert tester.send_xml(make_xml("00000"))._args['content'] == u"未找到对应课程"


def test_dining_query():
    reply = tester.send_xml(make_xml("hunan"))._args['content']
    assert "Hunan Express" in reply
    assert "营业" in reply or "关门" in reply

    reply = tester.send_xml(make_xml("hunan express"))._args['content']
    assert "Hunan Express" in reply
    assert "营业" in reply or "关门" in reply

    reply = tester.send_xml(make_xml("revolution"))._args['content']
    assert "Revolution Noodle" in reply
    assert "营业" in reply or "关门" in reply

    reply = tester.send_xml(make_xml("Revo"))._args['content']
    assert "Revolution Noodle" in reply
    assert "营业" in reply or "关门" in reply


def test_unknown_query():
    reply = tester.send_xml(make_xml("xxxxxxxxxxxxx"))._args['content']
    assert reply == "无法解析查询"
