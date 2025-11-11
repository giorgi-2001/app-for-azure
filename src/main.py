import json

from flask import Flask, render_template

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler

from logger import connection_string, logger
from images.bp import bp as images_bp


app = Flask(__name__)


middleware = FlaskMiddleware(
    app,
    exporter=AzureExporter(connection_string=connection_string),
    sampler=ProbabilitySampler(rate=1.0),
)


app.register_blueprint(images_bp)


@app.errorhandler(500)
def handle_exception(e):
    logger.exception(json.dumps({
        "event": "error",
        "error": str(e)
    }))
    return {"error": "Internal Server Error"}, 500


@app.get("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
