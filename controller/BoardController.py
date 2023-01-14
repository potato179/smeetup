import datetime

import board as board
from werkzeug.security import generate_password_hash
from flask import request, flash, session, render_template
from flask_restx import Namespace, Resource, fields
from model.models import User, Region, Board
from app import db
import logging


article = Namespace(name="게시물 API",
                    path="/",
                    discription="게시물 API입니다")

write_model = article.model(
    "articleWrite", {
        "title": fields.String(description="제목", required=True, example="HELLO S-meetUP !"),
        "body": fields.String(description="내용", required=False, example="스밋업"),
        "writer": fields.String(description="작성자", required=False, example="SmeetUP 대표 최현담")
    }
)


@board.routes("/Board/write")
class ArtWrite(Resource):
    # noinspection PyMethodMayBeStatic
    @board.expect(write_model)
    def post(self):
        param = request.get_json()

        userEntity = User.query.filter_by(name=param["writer"]).first()
        now = datetime.now()
        date = now.year + "년 " + now.month + "월 " + now.day + "일"

        artEntity = Board(title=param['title'],
                          body=param['body'],
                          user=userEntity,
                          reg_date=date,
                          views=0)
        db.session.add(artEntity)
        db.session.commit()

        responseArt = Board.query.filter_by(title=artEntity.title).first()

        return render_template("", article=responseArt)

# @board.routes("/Board/list")
# class ArtList(Resource):
#     # noinspection PyMethodMayBeStatic
#     @board.expect()