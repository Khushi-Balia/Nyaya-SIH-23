from flask import Flask, request, jsonify, make_response
from db import users
from bson import ObjectId
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)

CORS(app)
bcrypt = Bcrypt(app)

app.config["SECRET_KEY"] = "b71ec8224bea404e9c221bd88109da29"


@app.route("/users/signup", methods=["POST"])
def signup():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    existing_user = users.find_one({"email": email})
    if existing_user:
        response = make_response(
            jsonify({"success":False,"msg": "User already exists!Login Instead"}),
            409,
        )
        return response

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    id = users.insert_one(
        {"name": name, "email": email, "password": hashed_password}
    ).inserted_id
    if id:
        token = jwt.encode(
            {"email": email, "exp": datetime.utcnow() + timedelta(hours=24)},
            app.config["SECRET_KEY"],
        )

        # print(token)
        response = make_response(
            jsonify({"success":True,"msg": "User registered successfully"}),
            200,
        )
        response.set_cookie(
            "token", token, expires=datetime.utcnow() + timedelta(hours=24)
        )
        return response

    return jsonify({"success":False,"msg": "Sign Up failed"}), 400


@app.route("/users/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    existing_user = users.find_one({"email": email})
    if not existing_user:
        return jsonify({"success":False,"msg": "User does not exist!Signup instead!"}), 400

    hashed_password = existing_user["password"]
    check_password = bcrypt.check_password_hash(hashed_password, password)
    if check_password:
        token = jwt.encode(
            {"email": email, "exp": datetime.utcnow() + timedelta(hours=24)},
            app.config["SECRET_KEY"],
        )
        response = make_response(
            jsonify({"success":True,"msg": "Logged in successfully"}),
            200,
        )
        response.set_cookie(
            "token", token, expires=datetime.utcnow() + timedelta(hours=24)
        )

        return response

    elif not check_password:
        return (
            jsonify({"success":False,"msg": "Incorrect email or password!"}),
            400,
        )
    return jsonify({"success":False,"msg": "Login failed"}), 400


@app.route("/users/logout", methods=["POST"])
def logout():
    response = jsonify({"success":True,"msg": "Logout successful"})
    response.set_cookie("token", "", expires=0)
    return response


@app.route("/users/me")
def profile():
    token_cookie = request.cookies.get("token")
    if not token_cookie:
        return jsonify({"success":False,"msg": "User not logged in"}), 401

    try:
        decoded = jwt.decode(
            token_cookie, app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        email = decoded.get("email")
        existing_user = users.find_one({"email": email})
        user = {"name": existing_user["name"], "email": existing_user["email"]}
        return jsonify({"success":True,"user": user, "msg": "User authenticated successfully"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"success":False,"msg": "Token has expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"success":False,"msg": "Invalid token"}), 401
    

@app.route("/users/deleteprofile")
def deleteprofile():
    token_cookie = request.cookies.get("token")
    if not token_cookie:
        return jsonify({"success":False,"msg": "User not logged in"}), 401

    try:
        decoded = jwt.decode(
            token_cookie, app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        email = decoded.get("email")
        existing_user = users.find_one({"email": email})
        user = {"name": existing_user["name"], "email": existing_user["email"]}
        users.delete_one(existing_user)
        response = jsonify({"success":True,"user": user, "msg": "User deleted successfully"})
        response.set_cookie("token", "", expires=0)
        return response,200
    except jwt.ExpiredSignatureError:
        return jsonify({"success":False,"msg": "Token has expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"success":False,"msg": "Invalid token"}), 401
    

@app.route("/users/updateprofile",methods=["POST"])
def updateprofile():
    token_cookie = request.cookies.get("token")
    if not token_cookie:
        return jsonify({"success":False,"msg": "User not logged in"}), 401

    try:
        decoded = jwt.decode(
            token_cookie, app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        email = decoded.get("email")
        updated_name=request.json["name"]
        users.update_one({"email": email},{ "$set": { "name": updated_name } })
        existing_user = users.find_one({"email": email})
        user = {"name": existing_user["name"], "email": existing_user["email"]}
        response = jsonify({"success":True,"user": user, "msg": "Username updated successfully"})
        return response,200
    except jwt.ExpiredSignatureError:
        return jsonify({"success":False,"msg": "Token has expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"success":False,"msg": "Invalid token"}), 401

@app.route("/users/updatepassword",methods=["POST"])
def updatepassword():
    token_cookie = request.cookies.get("token")
    if not token_cookie:
        return jsonify({"success":False,"msg": "User not logged in"}), 401
    try:
        oldpassword=request.json["oldpassword"]
        newpassword=request.json["newpassword"]
        confirmpassword=request.json["confirmpassword"]
        decoded = jwt.decode(
            token_cookie, app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        email = decoded.get("email")
        existing_user=users.find_one({"email":email})
        hashed_password = existing_user["password"]
        check_password = bcrypt.check_password_hash(hashed_password,oldpassword)
        if check_password==0:
            return jsonify({"success":False,"msg":"Please try again with the correct credentials"})   
        if newpassword!=confirmpassword:
            return jsonify({"success":False,"msg":"Please try again with the correct credentials"})    
        myquery = { "email": email}
        hashed_password = bcrypt.generate_password_hash(newpassword).decode("utf-8")
        newvalues = { "$set": { "password": hashed_password } }
        users.update_one(myquery, newvalues)
        return jsonify({"success":True,"msg":"Password updated sucessfully"}) , 200
    except jwt.ExpiredSignatureError:
        return jsonify({"success":False,"msg": "Token has expired"}), 401

    except jwt.InvalidTokenError:
        return jsonify({"success":False,"msg": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(debug=True, port=8000)
