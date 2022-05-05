from .controllers import ArticleController
from . import app

from flask import make_response, jsonify


@app.route("/article/<int:article_id>", methods=["GET"])
def get(article_id: int):
    article_controller = ArticleController()

    try:
        article = article_controller.get(article_id)

        return make_response(jsonify({
            "id": article.id,
            "title": article.title,
            "body": article.body
        }), 200)
    except Exception as e:
        return make_response(jsonify({
            "message": "Could not find resource",
            "data": None,
            "error": str(e)
        }), 405)
