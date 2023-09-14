from flask import Flask, request
from flask import render_template
from flask import current_app as app
import requests
from flask_restful import Api, Resource, fields, marshal_with, reqparse




@app.route("/admin", methods=["GET"])
def adminPage():
    # articles = Article.query.filter(Article.authors.any(username=user_name))
    return render_template("admin.html")

@app.route("/user/<user_id>", methods=["GET"])
def UserPage(user_id):
    user=User.query.filter_by(id=user_id).first()
    venues=requests.get('http://127.0.0.1:8080/venues',headers={'Accept': 'application/json'}).json()
    return render_template("user.html",user=user,venues=venues)




@app.route("/login_admin", methods=["GET"])
def loginAdmin():
    return render_template("adminLogin.html",form=LoginForm)

@app.route("/login_user", methods=["GET"])
def loginUser():
    return render_template("userLogin.html",form=LoginForm)

# @app.route("/search", methods=["GET"])
# def search():
#     #Get q from the get request, url parameter
#     q = request.args.get('q')
#     # q = "%q%"
#     #results = Article.query.filter(Article.content.like(q)).all()
#     results = ArticleSearch.query.filter(ArticleSearch.content.op("MATCH")(q)).all()    
#     print(results)
#     app.logger.debug("Inside get all results using debug")
#     return render_template("results.html", q=q, results=results)
