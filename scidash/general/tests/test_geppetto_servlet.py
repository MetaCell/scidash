from django.test import TestCase

from pygeppetto_gateway.base import GeppettoServletManager


class GeppettoServletTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(GeppettoServletTest, cls).setUpClass()
        cls.servlet_manager = GeppettoServletManager()

    def test_ws_address(self):
        self.assertEqual(
            self.servlet_manager.host,
            "ws://scidash-virgo:8080/org.geppetto.frontend/GeppettoServlet")
