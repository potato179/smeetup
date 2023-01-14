from werkzeug.security import generate_password_hash
from flask import request, flash, session
from flask_restx import Namespace, Resource, fields
from model.models import User, Region
from app import db
import logging


article = Namespace(name="게시물 API",
                    path="/",
                    discription="게시물 API입니다")

