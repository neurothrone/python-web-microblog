import datetime
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient

from post import Post


load_dotenv()


# Wrap everything in create_app() function (must be named as such) and return
# app at the end. Future proofing.
def create_app():
    app = Flask(__name__, template_folder="templates")
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def microblog_page():
        # Add a new post
        if request.method == "POST":
            content = request.form.get("new_post_content")
            date = datetime.datetime.today()
            new_post = Post(title="Title", date=date, content=content)
            app.db.posts.insert_one({"title": "Title", "date": new_post.date, "content": new_post.content})

        # Get all posts from DB
        retrieved_posts = [post for post in app.db.posts.find({})]

        # Create a list of Post objects from the retrieved data
        all_posts = []
        for post in retrieved_posts:
            current_post = Post(title=post["title"],
                                content=post["content"],
                                date=post["date"])
            all_posts.append(current_post)

        return render_template("microblog.html", posts=all_posts.__reversed__())
    return app


if __name__ == "__main__":
    application = create_app()
    application.run()
