import json

from werkzeug.security import generate_password_hash
from flask import request, flash, session, Response, jsonify, render_template
from flask_restx import Namespace, Resource, fields
from model.models import User, Region, Review
from app import db

user = Namespace(name="회원가입, 로그인 API",
                 path="/",
                 discription="회원가입 로그인 API입니다")

user_model = user.model(
    "User", {
        "regionName": fields.String(description="지역명", required=True, example="Seoul"),
        "username": fields.String(description='사용자 이름(ID)', required=True, example="1234"),
        "password": fields.String(description="비밀번호", required=True, example="1234")
    }
)

login_model = user.model(
    "Login", {
        "username": fields.String(description='사용자 이름(ID)', required=True, example="1234"),
        "password": fields.String(description="비밀번호", required=True, example="1234")
    }
)

profile_model = user.model(
    "Profile", {
        "username": fields.String(description='사용자 이름(ID)', required=True, example="1234")
    }
)

review_model = user.model(
    "Review", {
        "targetName": fields.String(description='사용자 이름(ID)', required=True, example="1234"),
        "body": fields.String(description='후기 내용', required=True, example="1234"),
        "score": fields.Integer(description="평점", required=True, example=5)
    }
)


# 스웨거 적용 위해 클래스로 생성하기
@user.route('/sign-up')
class example(Resource):
    # noinspection PyMethodMayBeStatic
    @user.expect(user_model)
    def post(self):
        param = request.get_json()

        # 지역 엔티티 받아오기
        region = Region.query.filter_by(name=param['regionName']).first()

        if region is None:
            print("region Entity is None !")

        # 유저 DTO 생성
        userEntity = User(name=param["username"],
                          password=generate_password_hash(param["password"]),
                          region=region,
                          study_score=0)
        db.session.add(userEntity)
        db.session.commit()

        return {
            "id": userEntity.id,
            "name": userEntity.name,
            "password": userEntity.password,
            "region": region.name,
            "study_score": userEntity.study_score
        }


@user.route('/login')
class login(Resource):
    @user.expect(login_model)
    def post(self):
        param = request.get_json()
        error = None

        loginUser = User.query.filter_by(name=param["username"]).first()
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
                "study_score": loginUser.study_score,
                "error": error
            }
        else:
            flash(error)
            return {
                "id": None,
                "username": None,
                "password": None,
                "region": None,
                "study_score": None,
                "error": error
            }


@user.route("/logout")
class logout(Resource):
    def post(self):
        session.clear()
        return "로그아웃 성공"


@user.route("/profile")
class profile(Resource):
    @user.expect(profile_model)
    def post(self):
        param = request.get_json()

        userEntity = User.query.filter_by(name=param['username']).first()
        regionEntity = Region.query.filter_by(id=int(userEntity.region_id)).first()
        reviewEntity = Review.query.filter_by(user_id=userEntity.id).all()


@user.route("/review")
class review(Resource):
    @user.expect(review_model)
    def post(self):
        param = request.get_json()
        userEntity = User.query.filter_by(name=param['targetName']).first()
        reviewEntity = Review(user=userEntity,
                              body=param['body'],
                              score=param['score'])

        db.session.add(reviewEntity)
        db.session.commit()

        return render_template()
