#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    # using a get method to verify whether the user_id is in the session
    def get(self):
        user = User.query.filter(User.id == session.get("user_id")).first()
        #  using an if statement to ceck if the person actually is a user
        if user:
            return user.to_dict(), 200
        else:
            return {}, 204
                                    


    pass

class Login(Resource):
    #  using post method 
    def post(self):
        json = request.get_json()
        #  querying the database and posting the username
        user = User.query.filter(User.username == json["username"]).first()
        password = json['password']
        if user.authenticate(password):
            session["user_id"] = user.id
            return user.to_dict(), 200
        else:
            return {'error': 'Invalid username or password'}, 401

    pass

class Logout(Resource):
    def delete(self):
        session["user_id"] = None
        return {'message': '204: No Content'}, 204
    pass

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, "/check_session", endpoint="check_session")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
