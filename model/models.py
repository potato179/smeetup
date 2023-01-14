from app import db


# 게시판
class Board(db.Model):
    __tablename__ = 'board'
    # ID 식별자
    id = db.Column(db.Integer, primary_key=True)
    # 제목 ( 스터디 구인글 )
    title = db.Column(db.String(200), nullable=False, unique=True)
    # 내용
    body = db.Column(db.Text(), nullable=False)
    # 조회수
    views = db.Column(db.Integer, nullable=False)
    # 게시일 ( 작성일 )
    reg_date = db.Column(db.DateTime(), nullable=False)
    # 유저 ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('board'))
    keyword = db.Column(db.String(200))


# 유저
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    study_score = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer)
    # 지역 ID
    region_id = db.Column(db.Integer, db.ForeignKey('region.id', ondelete='CASCADE'), nullable=False)
    region = db.relationship('Region')


# 지역
class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    # 지역명
    name = db.Column(db.String(150), unique=True, nullable=False)


# 유저 공부이력
class StudyResume(db.Model):
    __tablename__ = 'study_resume'
    id = db.Column(db.Integer, primary_key=True)
    # 유저 ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('study_resume'))
    # 이력 내용
    content = db.Column(db.Text(), nullable=False)


# 유저 후기
class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    # 대상 유저 (FK)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('review'))
    # 후기 내용
    body = db.Column(db.Text(), nullable=False)
    # 평점
    score = db.Column(db.Integer, nullable=False)
