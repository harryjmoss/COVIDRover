import flask
from covidrover import create_app


class TestApp:
    app = create_app(dev=True)
    # app.template_folder='covidrover/templates/'
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    test_app = app.test_client()

    def test_flaskapp(self):

        assert not isinstance(self.test_app, type(None))

    def test_home(self):
        response = self.test_app.get("/", content_type="html/text")
        assert response.status_code == 200

    def test_casesimd(self):
        response = self.test_app.get("/casesvsimd", content_type="html/text")
        assert response.status_code == 200

    def test_deathsdecile(self):
        response = self.test_app.get("/deathsvsdecile", content_type="html/text")
        assert response.status_code == 200

    def test_casesmap(self):
        response = self.test_app.get("/plotcases", content_type="html/text")
        assert response.status_code == 200

    def test_imdmap(self):
        response = self.test_app.get("/plotimd", content_type="html/text")
        assert response.status_code == 200

    def test_imdnormmap(self):
        response = self.test_app.get("/plotimdnorm", content_type="html/text")
        assert response.status_code == 200

    def test_404(self):
        response = self.test_app.get("a", content_type="html/text")
        assert response.status_code == 404
