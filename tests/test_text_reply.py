from tests.test_configs import tester, make_xml


def test_text_reply():
    reply = tester.send_xml(make_xml("15213"))._args['content']
    assert "15213" in reply
    assert "课号" in reply
    assert "评分" in reply
    print("You can manually check reply below: ")
    print(reply)

    assert tester.send_xml(make_xml("00000"))._args['content'] == u"未找到对应课程"
