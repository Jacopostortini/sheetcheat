from flask_restful import Resource, request
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                get_raw_jwt)
from models.users import UserModel
import hashlib
import datetime
from datetime import timedelta
import time
from flask import render_template


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        mail = data['mail']
        password = data['password']
        user = UserModel.find_by_mail(mail)
        epsw = password.encode('utf-8')
        if user and user.password == hashlib.sha512(epsw).hexdigest():  # and user.confirmed==True:
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=user.id, expires_delta=expires, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token,
                    "refresh_token": refresh_token,
                    "username": user.username
                    }, 200
        return {"message": "invalid credentials"}, 401

    def get(self):
        return render_template("home.html")


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        a = get_raw_jwt()
        user = UserModel.find_by_id(current_user)
        # return str(a["iat"])+" "+str(int(time.time()))
        # return str(user.password_change)+" "+str(a["iat"])
        if a["iat"] >= user.password_change:
            expires = datetime.timedelta(days=365)
            new_token = create_access_token(identity=current_user, fresh=False)
            return {"access_token": new_token}
        return "password was changed"
