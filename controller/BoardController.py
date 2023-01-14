import datetime

from flask import request, flash, session, g, jsonify
from flask_restx import Namespace, Resource, fields
from model.models import User, Region, Board
from app import db
from datetime import datetime
import sqlite3
import pandas as pd
import json
import logging

board = Namespace(name="게시물 API",
                  path="/",
                  discription="게시물 API입니다")

write_model = board.model(
    "write", {
        "title": fields.String(description="제목", required=True, example="HELLO S-meetUP !"),
        "body": fields.String(description="내용", required=False, example="스밋업"),
        "keyword": fields.String(description="키워드", required=False, example="#TEST")
    }
)

search_model = board.model(
    "search", {
        "keyword": fields.String(description="키워드 검색", example="#TEST"),
        "title": fields.String(description="제목 검색", example="HELLO"),
        "age": fields.Integer(description="나이 필터", example=15)
    }
)


@board.route("/boards")
class ArtWrite(Resource):
    # noinspection PyMethodMayBeStatic
    @board.expect(write_model)
    def post(self):
        param = request.get_json()
        g.user = User.query.get(session["user_id"])

        now = datetime.now()
        artEntity = Board(title=param['title'],
                          body=param['body'],
                          user_id=session["user_id"],
                          views=0,
                          reg_date=now,
                          keyword=param['keyword'],
                          user=g.user)
        db.session.add(artEntity)
        db.session.commit()

        return {
            "title": artEntity.title,
            "body": artEntity.body,
            "views": artEntity.views,
            "regDate": str(artEntity.reg_date),
            "writer": g.user.name,
            "keyword": artEntity.keyword,
        }

    def get(self):
        board_list = Board.query.order_by(Board.id.desc())
        con = sqlite3.connect("C:\\Users\\Yang\\Desktop\\Code\\Python\\StudyMatchingService\\pybo.db")

        # 질문 json 바인딩
        df = pd.read_sql(str(board_list.statement),
                         con,
                         board_list.session.bind) \
            .to_json(orient='records')

        return jsonify(json.loads(df))


@board.route("/Board/search")
class Search(Resource):
    @board.expect(search_model)
    def get(self):
        param = request.get_json()
        ageSearch = False
        if param['age'] is not None:
            ageSearch = True
        if not ageSearch:
            boardEntityList = Board.query \
                .join(User, Board.user_id == User.id) \
                .add_columns(Board.id, User.name, Board.title, Board.views, Board.reg_date, Board.keyword) \
                .filter(
                    Board.title.like(f"%{param['title']}%"),
                    Board.keyword.like(f"{param['keyword']}"),
                    User.age >= param['age'],
                    Board.user_id == User.id
                )
        else:
            boardEntityList = Board.query \
                .join(User, Board.user_id == User.id) \
                .add_columns(Board.id, User.name, Board.title, Board.views, Board.reg_date, Board.keyword) \
                .filter(
                    Board.title.like(f"%{param['title']}%"),
                    Board.keyword.like(f"{param['keyword']}"),
                    User.age >= param['age'],
                    Board.user_id == User.id
                )
        return
