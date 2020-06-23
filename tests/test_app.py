import flask
from covidrover import app
import runapp

class TestApp():

    def test_create_app(self):
        self.app = app.create_app()
        self.app.testing = True
        return self.app

    #def test_base_endpoint(self):
        
    #    test_app = flask.Flask(__name__)
     #   with test_app.test_client() as test_client:
    #        test_response = test_client.get('')
     #       assert test_response.status_code == 200

