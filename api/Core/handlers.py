from .controllers import ArticleController
from . import HttpRes, app


from flask import make_response, jsonify
from http import HTTPStatus


@app.route("/blog/article/<int:id>", methods=["GET"])
def get(id: int):
    article_controller = ArticleController()

    try:
        article = article_controller.get(id)

        return HttpRes(
            data={"title": article.title,
                  "body": article.body}
        ).make_response()
    except Exception as e:
        return HttpRes(
            code=HTTPStatus.NOT_FOUND
        ).make_response()


@app.route("/blog/articles/<int:filter>", methods=["GET"])
def get_all(filter: int):
    article_controller = ArticleController()

    try:
        articles = article_controller.get_filtered(filter)

        def _map_articles(articles):
            result = map(lambda a: {
                "id": a.id,
                "title": a.title,
                "body": a.body
            }, articles)

            return list(result)

        return HttpRes(
            data=_map_articles(articles)
        ).make_response()
    except Exception as e:
        return HttpRes(
            code=HTTPStatus.INTERNAL_SERVER_ERROR
        ).make_response()
