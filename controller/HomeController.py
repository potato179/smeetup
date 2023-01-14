from flask import Blueprint, render_template
from flask_restx import Namespace, Resource

bp = Blueprint('main', __name__, url_prefix="/")

home = Namespace(name='home',
                 path='/',
                 description="")


@home.route("/menu")
class example(Resource):
    def get(self):
        return render_template("main.html")
