# runs a test server for covidrover
from covidrover import create_app
app = create_app() # pass no argument here to get a prod environment, pass True to get a dev env


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

#if __name__ == "__main__":
 #   app.run()

#
