from Core import app, HttpRes, HTTPStatus
from Core.controllers import ArticleController
from Authentication.handlers import require_login
from flask import request, make_response, jsonify


@app.route("/builder/articles", methods=["GET"])
@require_login
def get_all_articles(user):
    article_controller = ArticleController()

    try:
        articles = article_controller.get_all_by_user(user)

        def _map_articles(articles):
            result = map(lambda a: {
                "title": a.title,
                "body": a.body
            }, articles)

            return list(result)

        return HttpRes(
            data=_map_articles(articles)
        ).make_response()
    except Exception as e:
        return HttpRes(
            err=str(e),
            code=HTTPStatus.IM_A_TEAPOT
        ).make_response()


@app.route("/builder/create", methods=["GET"])
@require_login
def create_article(user):
    article_controller = ArticleController()

    try:
        title = request.form["title"]
        body = request.form["body"]

        article_id = article_controller.create(title, body)

        return HttpRes(
            ok="Successfuly created",
            data={"id": article_id}
        ).make_response()
    except Exception as e:
        return HttpRes(
            err="Something went wrong while trying to create article",
            code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.route("/builder/edit/<int:article_id>", methods=["GET"])
@require_login
def edit_article(user, article_id):
    return make_response(jsonify({
        "email": user.email,
        "post-id": article_id
    }), 200)
