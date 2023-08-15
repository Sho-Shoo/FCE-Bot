from tests.test_configs import tester, make_xml


def test_test_reply():
    assert tester.send_xml(make_xml("hello"))._args['content'] == u"Hello world!"
