from .test_api import APITest

class Test_App(APITest):

    def test_app_creation(self):
        self.assertIsNotNone(self.app)
