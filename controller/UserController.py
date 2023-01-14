from werkzeug.security import generate_password_hash
from flask import request, flash, session, jsonify, logging, g
from flask_restx import Namespace, Resource, fields
from model.models import User as User2, Region, Review
import pandas as pd
import sqlite3
import json
from app import db

User = Namespace(name="회원가입, 로그인 API",
                 path="/",
                 discription="회원가입 로그인 API입니다")

user_model = User.model(
    "User", {
        "regionName": fields.String(description="지역명", required=True, example="Seoul"),
        "username": fields.String(description='사용자 이름(ID)', required=True, example="1234"),
        "password": fields.String(description="비밀번호", required=True, example="1234"),
        "age": fields.Integer(description="나이", required=True, example=17)
    }
)

login_model = User.model(
    "Login", {
        "username": fields.String(description='사용자 이름(ID)', required=True, example="1234"),
        "password": fields.String(description="비밀번호", required=True, example="1234")
    }
)

profile_model = User.model(
    "Profile", {
        "username": fields.String(description='사용자 이름(ID)', required=True, example="1234")
    }
)

review_model = User.model(
    "Review", {
        "body": fields.String(description='후기 내용', required=True, example="1234"),
        "score": fields.Integer(description="평점", required=True, example=5)
    }
)


# 스웨거 적용 위해 클래스로 생성하기
@User.route('/sign-up')
class Sign_up(Resource):
    # noinspection PyMethodMayBeStatic
    @User.expect(user_model)
    def post(self):
        param = request.get_json()

        # 지역 엔티티 받아오기
        region = Region.query.filter_by(name=param["regionName"]).first()
        print(region)
        # 유저 생성
        userEntity = User(name=param["username"],
                          password=generate_password_hash(param["password"]),
                          region_id=region.id,
                          study_score=0,
                          age=param['age'])
        db.session.add(userEntity)
        db.session.commit()

        return {
            "id": userEntity.id,
            "name": userEntity.name,
            "password": userEntity.password,
            "age": userEntity.age,
            "region": region.name,
            "study_score": userEntity.study_score
        }


@User.route('/login')
class Login(Resource):
    # noinspection PyMethodMayBeStatic
    @User.expect(login_model)
    def post(self):
        param = request.get_json()
        error = None

        loginUser = User2.query.filter_by(name=param["username"]).first()
        if not loginUser or loginUser is None:
            error = "아이디가 일치하지 않습니다"
        if error is None:
            session.clear()
            session["user_id"] = loginUser.id
            userRegion = Region.query.filter_by(id=int(loginUser.region_id)).first()

            return {
                "id": loginUser.id,
                "username": loginUser.name,
                "password": loginUser.password,
                "region": userRegion.name,
                "study_score": loginUser.study_score
            }
        else:
            flash(error)


@User.route("/logout")
class Logout(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self):
        session.clear()
        return {
            "result": "로그아웃 성공"
        }


@User.route("/profile")
class profileTest(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self):
        g.user = User2.query.get(session["user_id"])
        print(g.user.id)
        print(type(g.user.id))
        print(type(User2.id))

        # regionEntity = Region.query.filter_by(id=int(g.user.region_id)).first()

        review_list = Review.query \
            .join(User2, Review.user_id == User2.id)

        print(review_list)

        con = sqlite3.connect("C:\\Users\\Yang\\Desktop\\Code\\Python\\StudyMatchingService\\pybo.db")

        # 질문 json 바인딩
        # df1 = pd.read_sql(str(review_list.statement),
        #                   con,
        #                   review_list.session.bind) \
        #     .to_json(orient='records')

        user_list = User2.query.order_by(User2.id.desc())
        con = sqlite3.connect("C:\\Users\\Yang\\Desktop\\Code\\Python\\StudyMatchingService\\pybo.db")

        # 질문 json 바인딩
        df = pd.read_sql(str(user_list.statement),
                         con,
                         user_list.session.bind) \
            .to_json(orient='records')
        users = json.loads(df)

        df2 = pd.read_sql(str(review_list.statement),
                          con,
                          review_list.session.bind) \
            .to_json(orient='records')
        reviews = json.loads(df2)

        for i in users:
            i["reviews"] = reviews
        return jsonify(users)


@User.route("/review")
class reviewTest(Resource):
    # noinspection PyMethodMayBeStatic
    @User.expect(review_model)
    def post(self):
        param = request.get_json()
        g.user = User2.query.get(session["user_id"])

        reviews = Review(body=param["body"],
                         score=param["score"],
                         user=g.user)
        db.session.add(reviews)
        db.session.commit()

        return {
            "id": reviews.id,
            "body": reviews.body,
            "score": reviews.score,
            "user_id": g.user.id
        }
