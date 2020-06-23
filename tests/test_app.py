from flask import Flask
from covidrover import app

def test_create_app():
    assert app.create_app is not None
    

    